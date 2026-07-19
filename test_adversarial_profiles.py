"""
Adversarial / edge-case user profiles for stress-testing recommend_songs().

Run with:
    python test_adversarial_profiles.py
from the project root.
"""

from src.recommender import load_songs, recommend_songs

PROFILES = [
    (
        "Conflicting: lofi genre + happy mood + high energy",
        {"genre": "lofi", "mood": "happy", "energy": 0.9},
    ),
    (
        "Conflicting: ambient genre + intense mood + near-zero energy",
        {"genre": "ambient", "mood": "intense", "energy": 0.1},
    ),
    (
        "Conflicting: rock genre + chill mood + very high energy",
        {"genre": "rock", "mood": "chill", "energy": 0.95},
    ),
    (
        "Out-of-range energy target (> 1.0)",
        {"genre": "pop", "mood": "happy", "energy": 1.7},
    ),
    (
        "Out-of-range energy target (negative)",
        {"genre": "pop", "mood": "happy", "energy": -0.5},
    ),
    (
        "Missing energy key (None)",
        {"genre": "pop", "mood": "happy", "energy": None},
    ),
    (
        "Case mismatch on genre/mood",
        {"genre": "POP", "mood": "Happy", "energy": 0.8},
    ),
    (
        "Missing genre key entirely",
        {"mood": "sad", "energy": 0.9},
    ),
    (
        "Unsupported mood value ('sad' not in catalog)",
        {"genre": "pop", "mood": "sad", "energy": 0.8},
    ),
    (
        "No preferences match anything",
        {"genre": "metal", "mood": "furious", "energy": 0.5},
    ),
]


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, prefs in PROFILES:
        print("\n" + "=" * 70)
        print(f"PROFILE: {label}")
        print(f"  prefs = {prefs}")
        print("-" * 70)

        try:
            recommendations = recommend_songs(prefs, songs, k=3)
        except Exception as exc:
            print(f"  !! CRASHED: {type(exc).__name__}: {exc}")
            continue

        if not recommendations:
            print("  (no recommendations returned)")
            continue

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"  {rank}. {song['title']} — {song['artist']}  (score: {score:.2f})")
            for reason in explanation.split("; "):
                print(f"       - {reason}")


if __name__ == "__main__":
    main()
