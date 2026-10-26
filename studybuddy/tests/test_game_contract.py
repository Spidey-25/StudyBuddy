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


if __name__ == "__main__":
    unittest.main()
