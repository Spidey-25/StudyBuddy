"""Opt-in smoke test against the configured local MySQL instance.

Run with PLATFORM_MYSQL_INTEGRATION=1. The created platform session is removed
in tearDown, so the seed teacher's progress stays unchanged.
"""
import os
import unittest
import uuid

from backend.app import app, db_connection, ensure_schema
from backend import game_catalog


def submit_action(client, session_id, payload, action_id=None):
    action_id = action_id or str(uuid.uuid4())
    return client.post(f"/api/game-sessions/{session_id}/action", json={**payload,"client_action_id":action_id}), action_id


@unittest.skipUnless(os.getenv("PLATFORM_MYSQL_INTEGRATION") == "1", "set PLATFORM_MYSQL_INTEGRATION=1 to use local MySQL")
class PlatformMySQLIntegrationTests(unittest.TestCase):
    def setUp(self):
        ensure_schema()
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.session_id = None
        self.session_ids = []
        self.legacy_session_ids = []
        self.created_user_id = None
        self.additional_user_ids = []
        self.created_subject_id = None
        self.created_game_id = None
        login = self.client.post("/api/login", json={"email": "teacher@example.com", "password": "Teacher@123"})
        self.assertEqual(login.status_code, 200, login.get_json())

    def tearDown(self):
        connection = db_connection()
        cursor = connection.cursor()
        for session_id in self.session_ids or ([self.session_id] if self.session_id else []):
            cursor.execute("DELETE FROM platform_game_sessions WHERE id=%s", (session_id,))
        for client_session_id in self.legacy_session_ids:
            cursor.execute("DELETE FROM study_sessions WHERE client_session_id=%s", (client_session_id,))
        if self.created_game_id:
            cursor.execute("DELETE FROM games WHERE id=%s", (self.created_game_id,))
        if self.created_subject_id:
            cursor.execute("DELETE FROM subjects WHERE id=%s", (self.created_subject_id,))
        if self.created_user_id:
            cursor.execute("DELETE FROM users WHERE id=%s", (self.created_user_id,))
        for extra_user_id in self.additional_user_ids:
            cursor.execute("DELETE FROM users WHERE id=%s", (extra_user_id,))
        connection.commit(); cursor.close(); connection.close()

    def test_platform_state_scoring_completion_and_duplicate_protection(self):
        started = self.client.post("/api/game-sessions", json={"game_id": "cpp-debugger"})
        self.assertEqual(started.status_code, 201, started.get_json())
        self.session_id = started.get_json()["session_id"]

        wrong, _ = submit_action(self.client,self.session_id,{"value":"wrong"})
        self.assertEqual(wrong.status_code, 200)
        self.assertFalse(wrong.get_json()["feedback"]["correct"])
        self.assertEqual(wrong.get_json()["state"]["level"], 0)

        for task_index in started.get_json()["state"]["level_order"]:
            answer = game_catalog.GAMES["cpp-debugger"]["levels"][task_index]["answer"]
            result, last_action_id = submit_action(self.client,self.session_id,{"value":answer})
            self.assertEqual(result.status_code, 200, result.get_json())
        self.assertTrue(result.get_json()["complete"])
        self.assertEqual(result.get_json()["state"]["score"], 400)

        saved = self.client.get(f"/api/game-sessions/{self.session_id}")
        self.assertTrue(saved.get_json()["complete"])
        self.assertEqual(saved.get_json()["mistakes"], 1)
        self.assertEqual(saved.get_json()["status"], "completed")
        self.assertEqual(saved.get_json()["accuracy"], 80)
        self.assertGreater(saved.get_json()["xp_awarded"], 0)
        duplicate, _ = submit_action(self.client,self.session_id,{"value":"different replay payload"},last_action_id)
        self.assertEqual(duplicate.status_code, 200)
        self.assertTrue(duplicate.get_json()["complete"])
        completed_action, _ = submit_action(self.client,self.session_id,{"value":"return a + b;"})
        self.assertEqual(completed_action.status_code, 409)
        connection = db_connection(); cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM platform_game_attempts WHERE platform_session_id=%s", (self.session_id,))
        self.assertEqual(cursor.fetchone()[0], 5)
        cursor.close(); connection.close()
        listed = self.client.get("/api/game-sessions").get_json()["sessions"]
        self.assertTrue(any(item["id"] == self.session_id and item["xp_awarded"] == saved.get_json()["xp_awarded"] for item in listed))

        other_user = app.test_client()
        login = other_user.post("/api/login", json={"email": "student@example.com", "password": "Student@123"})
        self.assertEqual(login.status_code, 200)
        self.assertEqual(other_user.get(f"/api/game-sessions/{self.session_id}").status_code, 404)
        old_subjects = [item["code"] for item in login.get_json()["user"]["subjects"]]
        try:
            self.assertEqual(other_user.post("/api/me/subjects", json={"subject_ids": []}).status_code, 200)
            self.assertEqual(other_user.post("/api/game-sessions", json={"game_id": "dsa-arena", "language": "C++"}).status_code, 403)
        finally:
            other_user.post("/api/me/subjects", json={"subject_ids": old_subjects})

    def test_catalog_routes_to_each_game_and_lifecycle_status_is_terminal(self):
        catalog = self.client.get("/api/game-catalog").get_json()["games"]
        self.assertEqual({game["id"] for game in catalog}, set(game_catalog.GAMES))
        self.assertEqual(self.client.post("/api/game-sessions", json={"game_id":"not-a-game"}).status_code, 404)
        first_id = None
        for card in catalog:
            started = self.client.post("/api/game-sessions", json={"game_id":card["id"], "language":"C++" if card["subject"]=="DSA" else ""})
            self.assertEqual(started.status_code, 201, (card["id"], started.get_json()))
            data = started.get_json()
            self.session_ids.append(data["session_id"])
            self.assertEqual(data["game"]["id"], card["id"])
            self.assertEqual(data["game"]["mechanic"], game_catalog.GAMES[card["id"]]["mechanic"])
            if first_id is None:
                first_id = data["session_id"]
            ended = self.client.post(f"/api/game-sessions/{data['session_id']}/exit", json={"status":"exited"})
            self.assertEqual(ended.status_code, 200, ended.get_json())
            self.assertEqual(ended.get_json()["status"], "exited")
            self.assertEqual(self.client.get(f"/api/game-sessions/{data['session_id']}").get_json()["status"], "exited")
            rejected, _ = submit_action(self.client,data["session_id"],{"value":"anything"})
            self.assertEqual(rejected.status_code, 409)
        repeated = self.client.post(f"/api/game-sessions/{first_id}/exit", json={"status":"abandoned"})
        self.assertEqual(repeated.get_json()["status"], "exited")

    def test_starting_a_different_game_abandons_the_old_active_session(self):
        first = self.client.post("/api/game-sessions", json={"game_id":"cpp-debugger"}).get_json()
        self.session_ids.append(first["session_id"])
        second = self.client.post("/api/game-sessions", json={"game_id":"python-logic"}).get_json()
        self.session_ids.append(second["session_id"])
        old = self.client.get(f"/api/game-sessions/{first['session_id']}").get_json()
        self.assertEqual(old["status"], "abandoned")
        rejected, _ = submit_action(self.client,first["session_id"],{"value":"return a + b;"})
        self.assertEqual(rejected.status_code, 409)
        self.assertEqual(self.client.get(f"/api/game-sessions/{second['session_id']}").get_json()["status"], "active")
        self.client.post(f"/api/game-sessions/{second['session_id']}/exit", json={"status":"abandoned"})

    def test_local_game_results_are_saved_once_with_abandonment_status(self):
        client_session_id = f"legacy-{uuid.uuid4().hex}"
        self.legacy_session_ids.append(client_session_id)
        payload = {"client_session_id":client_session_id,"subject_code":"PYTHON","game_type":"quiz","status":"completed","accuracy":75,"seconds":28,"points":245,"xp_awarded":12,"attempts":[{"topic":"Boolean logic","correct":True,"response_seconds":4},{"topic":"Boolean logic","correct":False,"response_seconds":8}]}
        created = self.client.post("/api/sessions", json=payload)
        self.assertEqual(created.status_code, 201, created.get_json())
        duplicate = self.client.post("/api/sessions", json=payload)
        self.assertEqual(duplicate.status_code, 200, duplicate.get_json())
        self.assertTrue(duplicate.get_json()["duplicate"])
        connection = db_connection(); cursor = connection.cursor()
        cursor.execute("SELECT id,status,accuracy,points,xp_awarded FROM study_sessions WHERE client_session_id=%s", (client_session_id,))
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 1)
        session_row = rows[0]
        cursor.execute("SELECT COUNT(*) FROM question_attempts WHERE session_id=%s", (session_row[0],))
        self.assertEqual(cursor.fetchone()[0], 2)
        cursor.close(); connection.close()
        self.assertEqual((session_row[1], float(session_row[2]), session_row[3], session_row[4]), ("completed", 75.0, 245, 12))
        invalid = self.client.post("/api/sessions", json={**payload,"status":"active"})
        self.assertEqual(invalid.status_code, 400)

    def test_registration_subjects_login_logout_and_teacher_permissions(self):
        email = f"e2e-{uuid.uuid4().hex[:12]}@example.test"
        registered = self.client.post("/api/register", json={"email":email,"display_name":"E2E Student","password":"Study@123","role":"student","branch":"cse"})
        self.assertEqual(registered.status_code, 201, registered.get_json())
        user = registered.get_json()["user"]
        self.created_user_id = user["id"]
        self.assertEqual(user["branch"], "cse")
        self.assertIn("DSA", [x["code"] for x in user["subjects"]])
        self.assertEqual(self.client.post("/api/me/subjects", json={"subject_ids":["DSA"]}).status_code, 200)
        self.assertEqual(self.client.post("/api/logout").status_code, 200)
        self.assertEqual(self.client.post("/api/login", json={"email":email,"password":"Study@123"}).status_code, 200)
        self.assertEqual(self.client.post("/api/login", json={"email":email,"password":"incorrect"}).status_code, 401)
        self.assertEqual(self.client.get("/api/teacher/analytics").status_code, 403)
        self.assertEqual(self.client.get("/api/teacher/games").status_code, 403)

    def test_dsa_language_persists_and_teacher_content_is_reviewable(self):
        missing = self.client.post("/api/game-sessions", json={"game_id":"dsa-arena"})
        self.assertEqual(missing.status_code, 400)
        started = self.client.post("/api/game-sessions", json={"game_id":"dsa-arena","language":"Java"})
        self.assertEqual(started.status_code, 201, started.get_json())
        self.session_id = started.get_json()["session_id"]
        self.assertEqual(started.get_json()["state"]["language"], "Java")
        self.assertEqual(self.client.get(f"/api/game-sessions/{self.session_id}").get_json()["game"]["language"], "Java")
        incorrect, _ = submit_action(self.client,self.session_id,{"value":[]})
        self.assertFalse(incorrect.get_json()["feedback"]["correct"])
        analytics = self.client.get("/api/teacher/analytics")
        self.assertEqual(analytics.status_code, 200, analytics.get_json())
        self.assertTrue(any(row["topic"] == "Algorithm Arena" for row in analytics.get_json()["weak_topics"]))

        code = f"TEST_{uuid.uuid4().hex[:8].upper()}"
        subject = self.client.post("/api/subjects", json={"name":"Temporary Test Subject","code":code,"branch":"cse"})
        self.assertEqual(subject.status_code, 201, subject.get_json())
        self.created_subject_id = subject.get_json()["id"]
        student = app.test_client()
        registration = student.post("/api/register", json={"email":f"subject-{uuid.uuid4().hex[:10]}@example.test","display_name":"Subject Student","password":"Subject@123","role":"student","branch":"cse"})
        self.assertEqual(registration.status_code, 201, registration.get_json())
        student_user = registration.get_json()["user"]
        self.additional_user_ids.append(student_user["id"])
        self.assertIn(code, [item["code"] for item in student_user["subjects"]])
        created = self.client.post("/api/games", json={"subject_id":self.created_subject_id,"title":"Temporary Teacher Stage","game_type":"quiz","content":{"questions":[{"prompt":"test"}]}})
        self.assertEqual(created.status_code, 201, created.get_json())
        self.created_game_id = created.get_json()["id"]
        listing = self.client.get("/api/teacher/games")
        self.assertTrue(any(row["id"] == self.created_game_id for row in listing.get_json()["games"]))


if __name__ == "__main__":
    unittest.main()
