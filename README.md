# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world music recommenders work in two stages. First, a **scoring** step looks at each song individually and asks "how well does this one song match this user?" using features of the song (genre, mood, energy) and of the user (favorite genre, current mood, target energy). Each song gets a number — and importantly, the scorer works one song at a time with no idea what else is in the pool. Second, a **ranking** step takes all the scored songs and turns them into the actual playlist — deciding order and cutoff for the final list. My version keeps that same two-stage structure at a smaller scale: a CSV catalog of songs, one user profile, a weighted scoring loop, and a top-K ranking.

**The flow:** Input (User Prefs) → Process (loop over every song in the CSV, scoring each one with the logic below) → Output (top K recommendations, sorted by score).

### Song features

- `title`, `artist` — identity
- `genre` — e.g. "pop", "rock", "lofi"
- `mood` — e.g. "happy", "chill", "hype"
- `energy` — 0–1 scale (as provided in the CSV)

### UserProfile features

- `favorite_genre` — the user's core taste
- `current_mood` — the vibe they want right now
- `target_energy` — 0–1, the energy level they're in the mood for

### Algorithm Recipe (finalized)

For each song in the catalog, the score is a weighted sum of three signals:

| Signal | Rule | Weight |
|---|---|---|
| Genre | +1 if `song.genre == user.favorite_genre`, else 0 | **2.0** |
| Mood | +1 if `song.mood == user.current_mood`, else 0 | **1.0** |
| Energy | `1 - abs(song.energy - user.target_energy)` (continuous) | **1.0** |

```
score = 2.0 * genre_match + 1.0 * mood_match + 1.0 * energy_closeness
```

**Why these weights:** genre is a stable, high-confidence signal — a user's favorite genre rarely changes — so it dominates. Mood is session-dependent (a pop lover can still want a chill song right now), so it nudges the ranking rather than controlling it. Energy is scored as *closeness* rather than an all-or-nothing bonus, so a near-exact energy match earns almost a full point and a mismatch decays smoothly instead of dropping to zero like genre/mood do.

After scoring, the ranking step sorts all songs by score (highest first) and returns the top K.

### Potential biases

- **Genre over-prioritization:** a genre match alone (2.0) can outweigh a strong mood + energy match, so great songs outside the user's favorite genre will struggle to break into the top K even when they nail the user's current vibe.
- **Mood may be too quiet:** if changing the user's mood (but not genre) doesn't shift the top-K list on the 10-song catalog, mood's weight is effectively too low. That's my test for whether 1.0 is the right weight.
- **No diversity control:** since ranking is a pure sort-by-score, the top K could all be the same artist or genre — nothing in the recipe prevents a repetitive playlist.
- **Small catalog sensitivity:** with only ~10 songs, ties and near-ties are common, and results depend heavily on how the catalog was hand-picked.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



