from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    points: int
    accuracy: int
    speed_bonus: int


def calculate_score(correct: int, total: int, seconds: int, seconds_per_item: int = 30) -> Score:
    total = max(total, 0)
    correct = max(0, min(correct, total))
    accuracy = round(correct / total * 100) if total else 0
    speed_bonus = max(0, round((total * seconds_per_item - max(seconds, 0)) * 2))
    return Score(correct * 100 + accuracy * 2 + speed_bonus, accuracy, speed_bonus)


def adaptive_multiplier(accuracy: float, median_seconds: float, repeated_mistakes: int) -> float:
    multiplier = 1.0
    if accuracy >= 85 and median_seconds <= 20:
        multiplier += 0.2
    elif accuracy < 60 or repeated_mistakes >= 2:
        multiplier -= 0.2
    return max(0.8, min(1.2, multiplier))
