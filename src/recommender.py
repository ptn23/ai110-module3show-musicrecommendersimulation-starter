from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    Returns (total_score, list_of_reason_strings).
    """
    score = 0.0
    reasons = []

    # --- Categorical matches ---
    # Mood outweighs genre: mood describes the emotional experience directly;
    # genre is a broader style bucket that can contain many different moods.
    if user_prefs.get("genre") and song["genre"] == user_prefs["genre"]:
        score += 3.0
        reasons.append(f"genre match ({song['genre']}): +3.0")

    if user_prefs.get("mood") and song["mood"] == user_prefs["mood"]:
        score += 4.0
        reasons.append(f"mood match ({song['mood']}): +4.0")

    # --- Continuous similarity: weight × (1 - |user - song|) ---
    if "energy" in user_prefs:
        pts = 3.0 * (1 - abs(user_prefs["energy"] - song["energy"]))
        score += pts
        reasons.append(f"energy sim: +{pts:.2f}")

    if "valence" in user_prefs:
        pts = 2.0 * (1 - abs(user_prefs["valence"] - song["valence"]))
        score += pts
        reasons.append(f"valence sim: +{pts:.2f}")

    if "acousticness" in user_prefs:
        pts = 1.5 * (1 - abs(user_prefs["acousticness"] - song["acousticness"]))
        score += pts
        reasons.append(f"acousticness sim: +{pts:.2f}")

    if "danceability" in user_prefs:
        pts = 1.0 * (1 - abs(user_prefs["danceability"] - song["danceability"]))
        score += pts
        reasons.append(f"danceability sim: +{pts:.2f}")

    if "tempo_bpm" in user_prefs:
        pts = 0.5 * max(0, 1 - abs(user_prefs["tempo_bpm"] - song["tempo_bpm"]) / 40)
        score += pts
        reasons.append(f"bpm sim: +{pts:.2f}")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Returns a list of (song_dict, score, explanation) tuples, best first.
    """
    # Score every song — list comprehension builds the full results list
    # without mutating the original `songs` list.
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # sorted() returns a NEW list sorted by score descending.
    # .sort() would sort in-place and return None — fine here, but
    # sorted() is preferred when the caller's list should stay unchanged.
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    return ranked[:k]
