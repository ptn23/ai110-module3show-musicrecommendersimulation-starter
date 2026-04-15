# Music Recommender Simulation

## Project Summary

This project builds a content-based music recommender system in Python. Given a user taste profile
(preferred genre, mood, energy level, and other audio features), the system scores every song in a
20-song catalog using a weighted proximity formula and returns the top-k matches ranked from best
to worst.

The system runs entirely from the command line (`python src/main.py`) and prints a formatted card
for each recommended song showing the title, artist, genre, mood, final score, and a bullet-point
breakdown of exactly why each song was chosen.

---

## How The System Works

Each `Song` stores seven attributes loaded directly from `data/songs.csv`:

| Attribute | Type | Description |
|---|---|---|
| `genre` | text | Style label (pop, lofi, rock, blues, etc.) |
| `mood` | text | Emotional tone (happy, chill, intense, melancholic, etc.) |
| `energy` | 0–1 float | Arousal / intensity level |
| `valence` | 0–1 float | Emotional positivity (high = bright, low = dark) |
| `acousticness` | 0–1 float | Organic vs. electronic texture |
| `danceability` | 0–1 float | Rhythmic engagement |
| `tempo_bpm` | integer | Beats per minute |

A `UserProfile` stores the listener's preferences using the same fields as optional keys in a
dictionary. Any feature omitted from the profile is simply skipped during scoring.

The `Recommender` computes a score for each song using two types of signals:

**Categorical bonuses (flat points):**
- Mood match: **+4.0 pts** — mood captures the emotional experience directly
- Genre match: **+1.5 pts** — genre is a broad style bucket, used as a weak tiebreaker

**Continuous proximity (weight x closeness):**

```
feature_score = weight x (1 - |user_preference - song_value|)
```

| Feature | Weight | Max pts |
|---|---|---|
| energy | 6.0 | 6.0 |
| valence | 2.0 | 2.0 |
| acousticness | 1.5 | 1.5 |
| danceability | 1.0 | 1.0 |
| tempo_bpm | 0.5 | 0.5 |

Maximum possible score: **16.5 pts** (all features match perfectly + mood + genre).

Songs are ranked by total score descending; the top-k results are returned.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python src/main.py
   ```

### Running Tests

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

**Experiment 1 — Swapping mood and genre weights**
Originally genre was worth +4.0 and mood +2.0. After swapping them (mood=4.0, genre=3.0), the
system started correctly preferring a jazz song over a rock song for a "relaxed" listener even
though neither matched genre. Mood proved to be a stronger signal than style label.

**Experiment 2 — Doubling energy, halving genre**
Energy weight was raised from 3.0 to 6.0 and genre was dropped from 3.0 to 1.5. This made
energy the single most powerful feature — a 0.5 mismatch on energy now costs 3.0 pts, more than
a full genre match is worth. Songs at the extreme ends of the energy scale (metal, lofi) separated
more clearly.

**Experiment 3 — Adversarial profiles**
Three edge-case profiles exposed scoring weaknesses:
- *High energy + melancholic mood*: the 4-pt mood bonus pulled a slow blues song to #1 even
  though the user wanted high-energy music — mood dominated energy.
- *All-neutral profile (everything 0.5)*: mid-range lofi and country songs won by default because
  they sit closest to the 0.5 midpoint — the system silently biases toward mid-catalog songs.
- *Genre/mood mismatch (classical + angry)*: no song matched both labels, so the top results
  split between an energy match (Iron Veil) and a genre match (Moonlit Sonata, energy=0.24)
  — a clearly wrong recommendation.

---

## Limitations and Risks

- **Tiny catalog** — 20 songs cannot represent the diversity of real music. Many user profiles
  will get "best available" results that are still a poor match.
- **Flat mood bonus can override numeric features** — a 4-pt mood match outweighs a 3-pt energy
  mismatch penalty, meaning the system can recommend a slow blues song to someone asking for
  high-energy music if the mood label matches.
- **Genre is a coarse label** — "pop" contains happy, sad, intense, and chill songs. A genre match
  means very little about whether the sound actually fits the user.
- **No diversity enforcement** — the same artist or genre can dominate all five slots if their
  songs happen to be numerically closest.
- **Self-reported preferences are noisy** — users may not know their own valence or acousticness
  preferences, and the system has no way to learn from feedback.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender made it clear that every number in a scoring formula is a design
decision with real consequences. Choosing to weight mood at 4.0 and genre at 1.5 was not
arbitrary — it reflects a claim that emotional tone matters more than style label. When the
adversarial tests revealed that a slow blues song could beat a metal track for a "high energy +
melancholic" user, it showed that a single strong categorical signal can override several numeric
features. Real recommenders like Spotify face the same tension at massive scale, which is why
they rely on implicit feedback (play counts, skips) rather than self-reported labels.

The clearest bias risk is the mid-range default: when a user gives no strong signal, the system
quietly favors songs with average feature values. In a real product, that would mean certain
genres (lofi, country) get systematically over-recommended to undecided users — not because they
are better, but because they are mathematically closer to the neutral midpoint.
