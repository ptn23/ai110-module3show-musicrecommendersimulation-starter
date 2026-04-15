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

    # ------------------------------------------------------------------ #
    # Header
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 52)
    print("  MUSIC RECOMMENDER — Top Picks")
    print(f"  Profile: genre={user_prefs.get('genre')}  "
          f"mood={user_prefs.get('mood')}  "
          f"energy={user_prefs.get('energy')}")
    print("=" * 52)

    # ------------------------------------------------------------------ #
    # One block per recommended song
    # ------------------------------------------------------------------ #
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Genre: {song['genre']}   Mood: {song['mood']}")
        print(f"    Score: {score:.2f}")
        print("    Why:")
        for reason in explanation.split(", "):
            print(f"      • {reason}")

    print("\n" + "=" * 52 + "\n")


if __name__ == "__main__":
    main()
