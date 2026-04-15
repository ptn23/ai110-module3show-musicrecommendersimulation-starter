"""
Command line runner for the Music Recommender Simulation.

Demonstrates three ranking strategies (Mood-First, Genre-First, Energy-Focused)
by running the same profile through each and printing results side by side.
"""

from recommender import load_songs, recommend_songs, MOOD_FIRST, GENRE_FIRST, ENERGY_FOCUSED


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "label":        "High-Energy Pop",
    "genre":        "pop",
    "mood":         "happy",
    "energy":       0.90,
    "valence":      0.85,
    "danceability": 0.88,
}

CHILL_LOFI = {
    "label":        "Chill Lofi",
    "genre":        "lofi",
    "mood":         "chill",
    "energy":       0.38,
    "valence":      0.60,
    "acousticness": 0.80,
}

DEEP_INTENSE_ROCK = {
    "label":        "Deep Intense Rock",
    "genre":        "rock",
    "mood":         "intense",
    "energy":       0.92,
    "valence":      0.35,
    "tempo_bpm":    150,
}

CONFLICTED_ENERGY_SAD = {
    "label":    "Adversarial — High Energy + Melancholic Mood",
    "mood":     "melancholic",
    "energy":   0.95,
    "valence":  0.25,
}

ALL_NEUTRAL = {
    "label":        "Adversarial — All Neutral",
    "energy":       0.50,
    "valence":      0.50,
    "acousticness": 0.50,
    "danceability": 0.50,
}

GENRE_MOOD_MISMATCH = {
    "label":   "Adversarial — Classical + Angry",
    "genre":   "classical",
    "mood":    "angry",
    "energy":  0.90,
    "valence": 0.20,
}

PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    CONFLICTED_ENERGY_SAD,
    ALL_NEUTRAL,
    GENRE_MOOD_MISMATCH,
]

# ---------------------------------------------------------------------------
# The three interchangeable strategies
# Swap this variable (or pass any strategy to recommend_songs) to change mode.
# ---------------------------------------------------------------------------
ACTIVE_STRATEGY = MOOD_FIRST   # <-- change to GENRE_FIRST or ENERGY_FOCUSED


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def print_results(user_prefs: dict, recommendations: list, strategy_name: str) -> None:
    """Print a formatted card for one profile + strategy combination."""
    label = user_prefs.get("label", "Unknown Profile")
    prefs_display = {k: v for k, v in user_prefs.items() if k != "label"}

    print("\n" + "=" * 60)
    print(f"  [{strategy_name}]  {label}")
    print(f"  Prefs: {prefs_display}")
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  --  {song['artist']}")
        print(f"       Genre: {song['genre']}   Mood: {song['mood']}")
        print(f"       Score: {score:.2f}")
        print("       Why:")
        for reason in explanation.split(", "):
            print(f"         * {reason}")

    print()


def compare_strategies(user_prefs: dict, songs: list, k: int = 3) -> None:
    """Run one profile through all three strategies and print a compact comparison."""
    label = user_prefs.get("label", "Profile")
    print("\n" + "#" * 60)
    print(f"  STRATEGY COMPARISON  |  {label}")
    print("#" * 60)

    for strategy in [MOOD_FIRST, GENRE_FIRST, ENERGY_FOCUSED]:
        results = recommend_songs(user_prefs, songs, k=k, strategy=strategy)
        titles = [f"#{i+1} {s['title']}" for i, (s, _, _) in enumerate(results)]
        print(f"\n  {strategy.name:<18} -> {' | '.join(titles)}")

    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Section 1: run every profile with the active strategy ---
    print("\n\n>>> SECTION 1: All profiles under ACTIVE STRATEGY =", ACTIVE_STRATEGY.name)
    for prefs in PROFILES:
        results = recommend_songs(prefs, songs, k=5, strategy=ACTIVE_STRATEGY)
        print_results(prefs, results, ACTIVE_STRATEGY.name)

    # --- Section 2: strategy comparison on the two most revealing profiles ---
    print("\n>>> SECTION 2: Strategy comparison (top 3 per strategy)")
    compare_strategies(DEEP_INTENSE_ROCK, songs)
    compare_strategies(CONFLICTED_ENERGY_SAD, songs)


if __name__ == "__main__":
    main()
