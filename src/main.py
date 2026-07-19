"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    header = f"Top {len(recommendations)} Recommendations"
    print("\n" + header)
    print("=" * len(header))

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Why:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


if __name__ == "__main__":
    main()
