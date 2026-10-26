import unittest

from backend.scoring import adaptive_multiplier, calculate_score


class ScoringTests(unittest.TestCase):
    def test_fast_perfect_score_beats_slow_perfect_score(self):
        self.assertGreater(calculate_score(5, 5, 20).points, calculate_score(5, 5, 140).points)

    def test_correct_answers_are_bounded(self):
        self.assertEqual(calculate_score(99, 5, 30).accuracy, 100)

    def test_adaptive_difficulty(self):
        self.assertGreater(adaptive_multiplier(95, 12, 0), 1)
        self.assertLess(adaptive_multiplier(40, 50, 3), 1)


if __name__ == "__main__":
    unittest.main()
