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
            for task_index in state["level_order"]:
                task = game["levels"][task_index]
                state, feedback = gc.apply_action(game_id, state, valid_action(game_id, task))
                self.assertTrue(feedback["correct"], (game_id, task, feedback))
            self.assertTrue(state["complete"], game_id)
            self.assertEqual(state["score"], len(state["level_order"]) * 100)

    def test_every_game_has_varied_levels_and_python_logic_has_a_real_bank(self):
        self.assertEqual(set(gc.ROTATING_LEVELS), set(gc.GAMES))
        for game_id, game in gc.GAMES.items():
            self.assertGreaterEqual(len(game["levels"]), 6, game_id)
            prompts = [level["prompt"] for level in game["levels"]]
            self.assertEqual(len(prompts), len(set(prompts)), game_id)
            self.assertTrue({"Easy", "Medium", "Hard"}.issubset({level["difficulty"] for level in game["levels"]}), game_id)
        self.assertGreaterEqual(len(gc.GAMES["python-logic"]["levels"]), 12)
        self.assertEqual({"Easy", "Medium", "Hard", "Expert"}, {level["difficulty"] for level in gc.GAMES["python-logic"]["levels"]})

    def test_each_session_selects_a_rotating_progressive_subset(self):
        game_id = "python-logic"
        state = gc.initial_state(game_id, previous_last=0)
        ordered = [gc.GAMES[game_id]["levels"][index]["difficulty"] for index in state["level_order"]]
        self.assertEqual(ordered, sorted(ordered, key={"Easy":0,"Medium":1,"Hard":2,"Expert":3}.get))
        self.assertNotEqual(state["level_order"][0], 0)
        self.assertEqual(len(state["level_order"]), 4)
        self.assertEqual(len(set(state["level_order"])), 4)
        self.assertTrue(set(state["level_order"]).issubset(range(len(gc.GAMES[game_id]["levels"]))))

    def test_reopening_each_game_includes_unseen_levels(self):
        for game_id, game in gc.GAMES.items():
            first = gc.initial_state(game_id)
            second = gc.initial_state(game_id, first["level_order"])
            self.assertEqual(len(first["level_order"]), 4, game_id)
            self.assertGreaterEqual(len(set(second["level_order"]) - set(first["level_order"])), 2, game_id)

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
                for private_key in ("answer", "correct", "target_force", "atoms", "bonds", "positions", "x", "y", "required", "conclusion", "tests", "test_cases"):
                    self.assertNotIn(private_key, level, (game_id, private_key))

    def test_code_edit_challenges_pass_private_test_suites_and_reject_bad_lines(self):
        from backend import code_checks
        count = 0
        for game_id, game in gc.GAMES.items():
            if game["mechanic"] != "code-edit":
                continue
            for index, task in enumerate(game["levels"]):
                self.assertGreaterEqual(code_checks.suite_size(game_id, index), 1, (game_id, index))
                self.assertTrue(code_checks.validate_code_edit(game_id, index, task["answer"], task["answer"]), (game_id, index))
                self.assertFalse(code_checks.validate_code_edit(game_id, index, "__import__('os').system('whoami')", task["answer"]), (game_id, index))
                count += code_checks.suite_size(game_id, index)
        self.assertEqual(count, 66)

    def test_expression_game_rejects_code_and_wrong_tiles(self):
        state = gc.initial_state("web-playground")
        state, result = gc.apply_action("web-playground", state, {"value": "__import__('os').system('whoami')"})
        self.assertFalse(result["correct"])

    def test_public_session_game_matches_private_action_order_without_answers(self):
        game_id = "python-logic"
        state = gc.initial_state(game_id)
        public = gc.public_session_game(game_id, state)
        for level_position, private_index in enumerate(state["level_order"]):
            self.assertEqual(public["levels"][level_position]["prompt"], gc.GAMES[game_id]["levels"][private_index]["prompt"])
            self.assertNotIn("answer", public["levels"][level_position])
        state, result = gc.apply_action("web-playground", state, {"value": "2+3+4"})
        self.assertFalse(result["correct"])


if __name__ == "__main__":
    unittest.main()
