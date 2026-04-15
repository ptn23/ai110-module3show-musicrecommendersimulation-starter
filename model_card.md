## Model Card

# Music Recommender Simulation — Model Card

## 1. Model Name

> VibeFinder 1.0

---

## 2. Intended Use

This system suggests up to 5 songs from a 20-song catalog based on a listener's preferred genre,
mood, energy, valence, acousticness, danceability, and tempo. It is a classroom simulation built
to explore how content-based recommenders work — it is not intended for real users or production
use.

---

## 3. How It Works

For each song in the catalog, the system computes a score by combining:

- A flat bonus if the song's mood matches the user's preferred mood (+4 pts)
- A flat bonus if the song's genre matches (+1.5 pts)
- A proximity score for each numeric feature: the closer the song's value is to the user's
  preference, the more points it earns (energy is weighted heaviest at 6x, down to tempo at 0.5x)

Songs are then sorted by total score and the top 5 are returned with an explanation showing how
each point was earned.

---

## 4. Data

- **20 songs** in `data/songs.csv` (10 original starter songs + 10 added to expand coverage)
- Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, metal, classical,
  hip-hop, r&b, country, reggae, blues, edm, folk, latin
- Moods represented: happy, chill, intense, relaxed, focused, moody, angry, romantic, confident,
  nostalgic, carefree, melancholic, euphoric, bittersweet, energetic
- The data reflects a general Western popular music taste profile; non-Western genres and
  regional styles are not represented

---

## 5. Strengths

- Works well for clear, consistent profiles — a "chill lofi" or "intense rock" user gets
  intuitively correct results with a large score gap between #1 and #5
- Every recommendation comes with an explanation — the user can see exactly which features drove
  the result
- Simple enough to audit by hand — any unexpected result can be traced back to a specific weight

---

## 6. Limitations and Bias

- The mood bonus (4 pts flat) can dominate all numeric features combined, producing wrong results
  when mood and energy point in opposite directions
- Songs with mid-range feature values (energy ~0.5, valence ~0.5) are systematically favored
  when the user profile is vague or incomplete
- The catalog has no songs outside Western pop/rock/electronic traditions, so users of those
  genres will always get poor matches
- All users are treated identically — there is no personalization from listening history

---

## 7. Evaluation

- Ran 6 user profiles (3 standard, 3 adversarial) and compared top-5 results against intuition
- Standard profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) all returned sensible #1
  picks with clear score separation
- Adversarial profiles revealed two failure modes: mood-energy conflict and mid-range default bias
- 2 pytest tests confirm that the OOP `Recommender` class sorts results correctly and returns
  non-empty explanations

---

## 8. Future Work

- Replace flat categorical bonuses with continuous similarity so mood and genre contribute
  proportionally rather than as binary on/off signals
- Add a diversity rule that prevents the same artist from appearing more than once in the top 5
- Incorporate implicit feedback (e.g., thumbs up/down) to adjust weights per user over time
- Expand the catalog to at least 100 songs covering non-Western and regional genres

---

## 9. Personal Reflection

How much a single weight value changes the feel of the entire system.
Doubling the energy weight from 3.0 to 6.0 made recommendations noticeably "stricter" about
tempo and intensity, which are songs that were formerly in the top 5 dropped out entirely. This mirrors
how real recommenders at companies like Spotify quietly shift what gets surfaced by tuning a
single internal parameter, often without users noticing.

Human judgment still matters most at the edges: deciding that mood should outweigh genre, or
that a "neutral" user should not silently be pushed toward mid-energy content, are ethical and
design choices that no formula can make on its own. The math executes whatever values the
designer chose.
