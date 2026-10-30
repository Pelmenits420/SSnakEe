"""Highscore saglabāšana lokālā JSON failā."""

import json
import os

FILE = "highscores.json"


def _default():
    return {"1p": 0, "2p": 0}


def load_scores():
    """Nolasa abu režīmu rekordus."""
    if not os.path.exists(FILE):
        return _default()
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key in _default():
                data.setdefault(key, 0)
            return data
    except (OSError, json.JSONDecodeError):
        return _default()


def save_score(mode, score):
    """Saglabā, ja jauns rekords."""
    scores = load_scores()
    if score > scores.get(mode, 0):
        scores[mode] = score
        try:
            with open(FILE, "w", encoding="utf-8") as f:
                json.dump(scores, f, indent=2)
        except OSError:
            pass
        return True
    return False