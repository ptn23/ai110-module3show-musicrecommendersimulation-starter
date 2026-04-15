"""
Command line runner for the Music Recommender Simulation.

Runs six user profiles — three standard and three adversarial — and
prints ranked top-5 results for each.
"""

from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "label":       "High-Energy Pop",
    "genre":       "pop",
    "mood":        "happy",
    "energy":      0.90,
    "valence":     0.85,
    "danceability": 0.88,
}

CHILL_LOFI = {
    "label":       "Chill Lofi",
    "genre":       "lofi",
    "mood":        "chill",
    "energy":      0.38,
    "valence":     0.60,
    "acousticness": 0.80,
}

DEEP_INTENSE_ROCK = {
    "label":       "Deep Intense Rock",
    "genre":       "rock",
    "mood":        "intense",
    "energy":      0.92,
    "valence":     0.35,
    "tempo_bpm":   150,
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles
# (designed to expose weaknesses or unexpected behaviour in scoring)
# ---------------------------------------------------------------------------

# 1. Conflicting energy vs mood:
#    energy=0.95 points at metal/EDM, but mood="melancholic" points at blues.
#    The system must choose — does high energy override a sad mood?
CONFLICTED_ENERGY_SAD = {
    "label":       "Adversarial — High Energy + Melancholic Mood",
    "mood":        "melancholic",
    "energy":      0.95,
    "valence":     0.25,
}

# 2. All-neutral profile:
#    Every numeric preference sits at 0.5 with no genre/mood hint.
#    Exposes whether the system produces a meaningful ranking or just
#    noise when given no signal to work with.
ALL_NEUTRAL = {
    "label":       "Adversarial — All Neutral (no preference signal)",
    "energy":      0.50,
    "valence":     0.50,
    "acousticness": 0.50,
    "danceability": 0.50,
}

# 3. Genre/mood mismatch:
#    genre="classical" but mood="angry" — no classical song in the catalog
#    carries an angry mood. Tests whether a genre orphan still surfaces
#    reasonable results via numeric features alone.
GENRE_MOOD_MISMATCH = {
    "label":       "Adversarial — Genre/Mood Mismatch (classical + angry)",
    "genre":       "classical",
    "mood":        "angry",
    "energy":      0.90,
    "valence":     0.20,
}

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    CONFLICTED_ENERGY_SAD,
    ALL_NEUTRAL,
    GENRE_MOOD_MISMATCH,
]


def print_results(user_prefs: dict, recommendations: list) -> None:
    """Print a formatted results block for one user profile."""
    label = user_prefs.get("label", "Unknown Profile")
    prefs_display = {k: v for k, v in user_prefs.items() if k != "label"}

    print("\n" + "=" * 56)
    print(f"  {label}")
    print(f"  Prefs: {prefs_display}")
    print("=" * 56)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}   Mood: {song['mood']}")
        print(f"       Score: {score:.2f}")
        print("       Why:")
        for reason in explanation.split(", "):
            print(f"         • {reason}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for prefs in PROFILES:
        recommendations = recommend_songs(prefs, songs, k=5)
        print_results(prefs, recommendations)


if __name__ == "__main__":
    main()
