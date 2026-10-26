"""Opt-in API-level end-to-end flow using the configured MySQL database."""
import os
import unittest
import uuid

from backend.app import app, db_connection, ensure_schema


@unittest.skipUnless(os.getenv("PLATFORM_MYSQL_INTEGRATION") == "1", "set PLATFORM_MYSQL_INTEGRATION=1 to use local MySQL")
class StudentJourneyEndToEndTests(unittest.TestCase):
    def setUp(self):
        ensure_schema()
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.user_id = None
        self.session_id = None

    def tearDown(self):
        if self.user_id:
            connection = db_connection(); cursor = connection.cursor()
            cursor.execute("DELETE FROM platform_game_sessions WHERE user_id=%s", (self.user_id,))
            cursor.execute("DELETE FROM users WHERE id=%s", (self.user_id,))
            connection.commit(); cursor.close(); connection.close()

    def test_register_choose_subject_play_save_progress_and_logout(self):
        email = f"journey-{uuid.uuid4().hex[:12]}@example.test"
        registered = self.client.post("/api/register", json={"email":email,"display_name":"Journey Student","password":"Journey@123","role":"student","branch":"cse"})
        self.assertEqual(registered.status_code, 201, registered.get_json())
        user = registered.get_json()["user"]
        self.user_id = user["id"]
        dsa = next(subject for subject in user["subjects"] if subject["code"] == "DSA")
        self.assertEqual(self.client.post("/api/me/subjects", json={"subject_ids":[dsa["id"]]}).status_code, 200)

        missing_language = self.client.post("/api/game-sessions", json={"game_id":"dsa-arena"})
        self.assertEqual(missing_language.status_code, 400)
        started = self.client.post("/api/game-sessions", json={"game_id":"dsa-arena","language":"C++"})
        self.assertEqual(started.status_code, 201, started.get_json())
        self.session_id = started.get_json()["session_id"]
        self.assertEqual(started.get_json()["state"]["language"], "C++")

        sequences = [
            ["Set low and high", "Compute midpoint", "Compare midpoint with target", "Discard the half that cannot contain target"],
            ["Enqueue the start node", "Dequeue the front node", "Visit each unvisited neighbour", "Enqueue those neighbours"],
        ]
        for sequence in sequences:
            result = self.client.post(f"/api/game-sessions/{self.session_id}/action", json={"value":sequence})
            self.assertEqual(result.status_code, 200, result.get_json())
            self.assertTrue(result.get_json()["feedback"]["correct"])

        saved = self.client.get(f"/api/game-sessions/{self.session_id}").get_json()
        self.assertTrue(saved["complete"])
        self.assertEqual(saved["game"]["language"], "C++")
        self.assertEqual(saved["score"], 200)
        self.assertTrue(any(item["id"] == self.session_id for item in self.client.get("/api/game-sessions").get_json()["sessions"]))
        self.assertTrue(any(item["game_id"] == "dsa-arena" for item in self.client.get("/api/game-progress").get_json()["progress"]))
        self.assertEqual(self.client.post("/api/logout").status_code, 200)
        self.assertEqual(self.client.get("/api/game-sessions").status_code, 401)


if __name__ == "__main__":
    unittest.main()
