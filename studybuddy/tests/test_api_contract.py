import unittest
from pathlib import Path
from backend.app import app


class ApiContractTests(unittest.TestCase):
    source = (Path(__file__).parents[1] / "backend" / "app.py").read_text(encoding="utf-8")

    def test_auth_subject_and_analytics_routes_exist(self):
        for route in ("/api/register", "/api/login", "/api/me/subjects", "/api/teacher/analytics"):
            self.assertIn(route, self.source)

    def test_schema_contains_relationship_tables(self):
        for table in ("user_subjects", "subjects", "games", "study_sessions", "question_attempts"):
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table}", self.source)

    def test_game_platform_routes_and_additive_session_table_exist(self):
        for route in ("/api/game-catalog", "/api/game-sessions", "/api/game-progress"):
            self.assertIn(route, self.source)
        self.assertIn("CREATE TABLE IF NOT EXISTS platform_game_sessions", self.source)

    def test_catalog_and_game_script_are_available_without_database_access(self):
        client = app.test_client()
        response = client.get("/api/game-catalog")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()["games"]), 32)
        script = client.get("/games.js")
        self.assertEqual(script.status_code, 200)
        script.close()

    def test_starting_a_game_requires_authentication(self):
        client = app.test_client()
        response = client.post("/api/game-sessions", json={"game_id": "cpp-debugger"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(client.get("/api/game-sessions").status_code, 401)


if __name__ == "__main__":
    unittest.main()
