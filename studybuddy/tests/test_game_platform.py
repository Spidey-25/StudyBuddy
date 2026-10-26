import unittest

from backend import game_catalog as gc


def valid_action(game_id, task):
    m = gc.GAMES[game_id]["mechanic"]
    if m in {"code-edit", "output-predict", "sql-query"}: return {"value": task["answer"]}
    if m in {"design-choice", "er-diagram", "diagnose", "ui-debug"}: return {"value": task["answer"]}
    if m == "numeric": return {"value": task["answer"]}
    if m == "logic-builder": return {"value": task["answer"]}
    if m == "order": return {"value": task["steps"]}
    if m == "structure-trace": return {"value": task["answer"]}
    if m == "schedule":
        return {"value": sorted((job.split()[0] for job in task["jobs"]), key=lambda name: int(next(x.split('(')[1].rstrip(')') for x in task["jobs"] if x.startswith(name))))}
    if m == "memory-allocation": return {"value": task["answer"]}
    if m == "route": return {"value": task["answer"]}
    raise AssertionError(m)


class GamePlatformTests(unittest.TestCase):
    def test_each_computing_subject_has_distinct_games(self):
        by_subject = {}
        for game_id, game in gc.GAMES.items():
            by_subject.setdefault(game["subject"], []).append((game_id, game["mechanic"]))
        self.assertEqual(set(by_subject), set(gc.SUBJECTS))
        for games in by_subject.values():
            self.assertGreaterEqual(len(games), 2)
            self.assertGreaterEqual(len({m for _, m in games}), 2)
        self.assertEqual(len(gc.GAMES), 32)
        self.assertNotIn("MATH", gc.SUBJECTS)

    def test_every_server_game_level_accepts_its_valid_action(self):
        for game_id, game in gc.GAMES.items():
            state = gc.initial_state(game_id)
            for task in game["levels"]:
                state, feedback = gc.apply_action(game_id, state, valid_action(game_id, task))
                self.assertTrue(feedback["correct"], (game_id, task, feedback))
            self.assertTrue(state["complete"], game_id)
            self.assertEqual(state["score"], len(game["levels"]) * 100)

    def test_wrong_answer_does_not_advance_and_records_mistake(self):
        state = gc.initial_state("cpp-debugger")
        state, result = gc.apply_action("cpp-debugger", state, {"value": "999"})
        self.assertFalse(result["correct"])
        self.assertEqual(state["level"], 0)
        self.assertEqual(state["mistakes"], 1)
        self.assertEqual(state["score"], 0)

    def test_public_catalog_does_not_include_server_answers(self):
        for game_id in gc.GAMES:
            for level in gc.public_game(game_id)["levels"]:
                for private_key in ("answer", "correct", "target_force", "atoms", "bonds", "positions", "x", "y", "required", "conclusion"):
                    self.assertNotIn(private_key, level, (game_id, private_key))

    def test_expression_game_rejects_code_and_wrong_tiles(self):
        state = gc.initial_state("web-playground")
        state, result = gc.apply_action("web-playground", state, {"value": "__import__('os').system('whoami')"})
        self.assertFalse(result["correct"])
        state, result = gc.apply_action("web-playground", state, {"value": "2+3+4"})
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
