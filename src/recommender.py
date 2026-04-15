from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Strategy pattern — each ScoringStrategy is a named set of weights.
# Pass one to score_song() or recommend_songs() to switch ranking behaviour.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ScoringStrategy:
    """Holds all scoring weights for one ranking mode."""
    name: str
    genre_pts: float        # flat bonus for a genre match
    mood_pts: float         # flat bonus for a mood match
    energy_w: float         # multiplier for energy proximity
    valence_w: float        # multiplier for valence proximity
    acousticness_w: float   # multiplier for acousticness proximity
    danceability_w: float   # multiplier for danceability proximity
    bpm_w: float            # multiplier for tempo proximity


# Mood is the primary lens — best for "how do I want to feel right now" users.
MOOD_FIRST = ScoringStrategy(
    name="Mood-First",
    genre_pts=1.5, mood_pts=5.0,
    energy_w=4.0, valence_w=3.0, acousticness_w=1.5,
    danceability_w=1.0, bpm_w=0.5,
)

# Genre anchors the result — best for "I only want rock / only want lofi" users.
GENRE_FIRST = ScoringStrategy(
    name="Genre-First",
    genre_pts=6.0, mood_pts=2.0,
    energy_w=3.0, valence_w=2.0, acousticness_w=1.5,
    danceability_w=1.0, bpm_w=0.5,
)

# Energy dominates — best for activity-based use (workout, study, sleep).
ENERGY_FOCUSED = ScoringStrategy(
    name="Energy-Focused",
    genre_pts=1.0, mood_pts=2.0,
    energy_w=8.0, valence_w=1.5, acousticness_w=1.0,
    danceability_w=1.0, bpm_w=1.0,
)

# Registry lets main.py look up a strategy by name string.
STRATEGIES: Dict[str, ScoringStrategy] = {
    s.name: s for s in [MOOD_FIRST, GENRE_FIRST, ENERGY_FOCUSED]
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the catalog of songs this recommender will rank."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs from the catalog ranked by score for this user."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string describing why this song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(
    user_prefs: Dict,
    song: Dict,
    strategy: ScoringStrategy = MOOD_FIRST,
) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the given strategy.
    Returns (total_score, list_of_reason_strings).
    """
    score = 0.0
    reasons = []

    # --- Categorical matches (flat bonuses defined by the strategy) ---
    if user_prefs.get("genre") and song["genre"] == user_prefs["genre"]:
        score += strategy.genre_pts
        reasons.append(f"genre match ({song['genre']}): +{strategy.genre_pts}")

    if user_prefs.get("mood") and song["mood"] == user_prefs["mood"]:
        score += strategy.mood_pts
        reasons.append(f"mood match ({song['mood']}): +{strategy.mood_pts}")

    # --- Continuous similarity: weight x (1 - |user - song|) ---
    if "energy" in user_prefs:
        pts = strategy.energy_w * (1 - abs(user_prefs["energy"] - song["energy"]))
        score += pts
        reasons.append(f"energy sim: +{pts:.2f}")

    if "valence" in user_prefs:
        pts = strategy.valence_w * (1 - abs(user_prefs["valence"] - song["valence"]))
        score += pts
        reasons.append(f"valence sim: +{pts:.2f}")

    if "acousticness" in user_prefs:
        pts = strategy.acousticness_w * (1 - abs(user_prefs["acousticness"] - song["acousticness"]))
        score += pts
        reasons.append(f"acousticness sim: +{pts:.2f}")

    if "danceability" in user_prefs:
        pts = strategy.danceability_w * (1 - abs(user_prefs["danceability"] - song["danceability"]))
        score += pts
        reasons.append(f"danceability sim: +{pts:.2f}")

    if "tempo_bpm" in user_prefs:
        pts = strategy.bpm_w * max(0, 1 - abs(user_prefs["tempo_bpm"] - song["tempo_bpm"]) / 40)
        score += pts
        reasons.append(f"bpm sim: +{pts:.2f}")

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: ScoringStrategy = MOOD_FIRST,
) -> List[Tuple[Dict, float, str]]:
    """
    Ranks all songs by score under the given strategy and returns the top-k.
    Returns a list of (song_dict, score, explanation) tuples, best first.
    """
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song, strategy)]
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
