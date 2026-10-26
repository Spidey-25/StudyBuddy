import unittest
from pathlib import Path


class GameContractTests(unittest.TestCase):
    source = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")
    platform_source = (Path(__file__).parents[1] / "frontend" / "games.js").read_text(encoding="utf-8")

    def test_core_game_modes_are_present(self):
        for mode in ("Quick Quiz", "Flashcard Review", "Challenge Mode", "Code Builder", "Fill Missing Lines", "Typing Sprint", "Memory Match"):
            self.assertIn(mode, self.source)

    def test_fill_game_has_explanations_and_objectives(self):
        self.assertIn("FILLBANK", self.source)
        self.assertIn("objective:", self.source)
        self.assertIn("submitTyping", self.source)

    def test_games_use_distinct_interactions(self):
        for interaction in ("memoryPick", "moveBuilder", "checkBuilder", "submitFill", "submitTyping"):
            self.assertIn(interaction, self.source)
        self.assertIn("Memory Match", self.source)
        for mechanic in ("output-predict", "structure-trace", "sql-query", "memory-allocation", "route", "ui-debug"):
            self.assertIn(mechanic, self.platform_source)

    def test_both_game_engines_close_sessions_on_navigation_and_retries_are_safe(self):
        self.assertIn("previous=='play'&&next!='play'", self.source)
        self.assertIn("finish(true,false)", self.source)
        self.assertIn("status:abandon?'abandoned':'completed'", self.source)
        self.assertIn("releasePlatformSession('abandoned')", self.source)
        self.assertIn("function exitPlatformGame()", self.source)
        self.assertIn("'/exit'", self.source)
        self.assertIn("client_session_id:ss.id", self.source)
        self.assertIn("INSERT IGNORE INTO study_sessions", (Path(__file__).parents[1] / "backend" / "app.py").read_text(encoding="utf-8"))

    def test_platform_completion_cannot_override_a_new_local_game(self):
        self.assertIn("if(cur=='play'&&platformSession&&!S.cur)", self.source)
        self.assertIn("if(S.cur)draw();else if(platformSession)drawPlatform()", self.source)
        self.assertIn("platformSession.status=d.status", self.source)
        self.assertIn("PLATFORM_RESULT_KEY", self.source)
        self.assertIn("releasePlatformSession('abandoned');localStorage.removeItem(PLATFORM_RESULT_KEY)", self.source)


if __name__ == "__main__":
    unittest.main()
