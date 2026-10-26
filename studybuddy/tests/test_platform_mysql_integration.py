"""Opt-in smoke test against the configured local MySQL instance.

Run with PLATFORM_MYSQL_INTEGRATION=1. The created platform session is removed
in tearDown, so the seed teacher's progress stays unchanged.
"""
import os
import unittest
import uuid

from backend.app import app, db_connection, ensure_schema


@unittest.skipUnless(os.getenv("PLATFORM_MYSQL_INTEGRATION") == "1", "set PLATFORM_MYSQL_INTEGRATION=1 to use local MySQL")
class PlatformMySQLIntegrationTests(unittest.TestCase):
    def setUp(self):
        ensure_schema()
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.session_id = None
        self.created_user_id = None
        self.additional_user_ids = []
        self.created_subject_id = None
        self.created_game_id = None
        login = self.client.post("/api/login", json={"email": "teacher@example.com", "password": "Teacher@123"})
        self.assertEqual(login.status_code, 200, login.get_json())

    def tearDown(self):
        connection = db_connection()
        cursor = connection.cursor()
        if self.session_id:
            cursor.execute("DELETE FROM platform_game_sessions WHERE id=%s", (self.session_id,))
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

        wrong = self.client.post(f"/api/game-sessions/{self.session_id}/action", json={"value": "wrong"})
        self.assertEqual(wrong.status_code, 200)
        self.assertFalse(wrong.get_json()["feedback"]["correct"])
        self.assertEqual(wrong.get_json()["state"]["level"], 0)

        for answer in ("return a + b;", "i < values.size()"):
            result = self.client.post(f"/api/game-sessions/{self.session_id}/action", json={"value": answer})
            self.assertEqual(result.status_code, 200, result.get_json())
        self.assertTrue(result.get_json()["complete"])
        self.assertEqual(result.get_json()["state"]["score"], 200)

        saved = self.client.get(f"/api/game-sessions/{self.session_id}")
        self.assertTrue(saved.get_json()["complete"])
        self.assertEqual(saved.get_json()["mistakes"], 1)
        duplicate = self.client.post(f"/api/game-sessions/{self.session_id}/action", json={"value": "i < values.size()"})
        self.assertEqual(duplicate.status_code, 409)
        listed = self.client.get("/api/game-sessions").get_json()["sessions"]
        self.assertTrue(any(item["id"] == self.session_id for item in listed))

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
        incorrect = self.client.post(f"/api/game-sessions/{self.session_id}/action", json={"value":[]})
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
