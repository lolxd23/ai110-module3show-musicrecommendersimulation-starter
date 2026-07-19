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
op 5 Recommendations
=====================

1. Sunrise City — Neon Echo
   Score: 3.98
   Why:
     - Matches favorite genre 'pop'
     - Matches preferred mood 'happy'
     - Energy 0.82 is close to target 0.80

2. Gym Hero — Max Pulse
   Score: 2.87
   Why:
     - Matches favorite genre 'pop'
     - Energy 0.93 is close to target 0.80

3. Rooftop Lights — Indigo Parade
   Score: 1.96
   Why:
     - Matches preferred mood 'happy'
     - Energy 0.76 is close to target 0.80

4. Night Drive Loop — Neon Echo
   Score: 0.95
   Why:
     - Energy 0.75 is close to target 0.80

5. Storm Runner — Voltline
   Score: 0.89
   Why:
     - Energy 0.91 is close to target 0.80
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I stress-tested the recommender with edge-case profiles: conflicting preferences, out-of-range and missing energy values, case mismatches, and preferences that match nothing in the catalog. Full terminal output below, followed by what I noticed.

```
======================================================================
PROFILE: Conflicting: lofi genre + happy mood + high energy
  prefs = {'genre': 'lofi', 'mood': 'happy', 'energy': 0.9}
----------------------------------------------------------------------
  1. Midnight Coding — LoRoom  (score: 2.52)
       - Matches favorite genre 'lofi'
       - Energy 0.42 is close to target 0.90
  2. Focus Flow — LoRoom  (score: 2.50)
       - Matches favorite genre 'lofi'
       - Energy 0.40 is close to target 0.90
  3. Library Rain — Paper Lanterns  (score: 2.45)
       - Matches favorite genre 'lofi'
       - Energy 0.35 is close to target 0.90

======================================================================
PROFILE: Conflicting: ambient genre + intense mood + near-zero energy
  prefs = {'genre': 'ambient', 'mood': 'intense', 'energy': 0.1}
----------------------------------------------------------------------
  1. Spacewalk Thoughts — Orbit Bloom  (score: 2.82)
       - Matches favorite genre 'ambient'
       - Energy 0.28 is close to target 0.10
  2. Storm Runner — Voltline  (score: 1.19)
       - Matches preferred mood 'intense'
       - Energy 0.91 is close to target 0.10
  3. Gym Hero — Max Pulse  (score: 1.17)
       - Matches preferred mood 'intense'
       - Energy 0.93 is close to target 0.10

======================================================================
PROFILE: Conflicting: rock genre + chill mood + very high energy
  prefs = {'genre': 'rock', 'mood': 'chill', 'energy': 0.95}
----------------------------------------------------------------------
  1. Storm Runner — Voltline  (score: 2.96)
       - Matches favorite genre 'rock'
       - Energy 0.91 is close to target 0.95
  2. Midnight Coding — LoRoom  (score: 1.47)
       - Matches preferred mood 'chill'
       - Energy 0.42 is close to target 0.95
  3. Library Rain — Paper Lanterns  (score: 1.40)
       - Matches preferred mood 'chill'
       - Energy 0.35 is close to target 0.95

======================================================================
PROFILE: Out-of-range energy target (> 1.0)
  prefs = {'genre': 'pop', 'mood': 'happy', 'energy': 1.7}
----------------------------------------------------------------------
  1. Sunrise City — Neon Echo  (score: 3.12)
       - Matches favorite genre 'pop'
       - Matches preferred mood 'happy'
       - Energy 0.82 is close to target 1.70
  2. Gym Hero — Max Pulse  (score: 2.23)
       - Matches favorite genre 'pop'
       - Energy 0.93 is close to target 1.70
  3. Rooftop Lights — Indigo Parade  (score: 1.06)
       - Matches preferred mood 'happy'
       - Energy 0.76 is close to target 1.70

======================================================================
PROFILE: Out-of-range energy target (negative)
  prefs = {'genre': 'pop', 'mood': 'happy', 'energy': -0.5}
----------------------------------------------------------------------
  1. Sunrise City — Neon Echo  (score: 3.00)
       - Matches favorite genre 'pop'
       - Matches preferred mood 'happy'
       - Energy 0.82 is close to target -0.50
  2. Gym Hero — Max Pulse  (score: 2.00)
       - Matches favorite genre 'pop'
       - Energy 0.93 is close to target -0.50
  3. Rooftop Lights — Indigo Parade  (score: 1.00)
       - Matches preferred mood 'happy'
       - Energy 0.76 is close to target -0.50

======================================================================
PROFILE: Missing energy key (None)
  prefs = {'genre': 'pop', 'mood': 'happy', 'energy': None}
----------------------------------------------------------------------
  1. Sunrise City — Neon Echo  (score: 3.00)
       - Matches favorite genre 'pop'
       - Matches preferred mood 'happy'
  2. Gym Hero — Max Pulse  (score: 2.00)
       - Matches favorite genre 'pop'
  3. Rooftop Lights — Indigo Parade  (score: 1.00)
       - Matches preferred mood 'happy'

======================================================================
PROFILE: Case mismatch on genre/mood
  prefs = {'genre': 'POP', 'mood': 'Happy', 'energy': 0.8}
----------------------------------------------------------------------
  1. Sunrise City — Neon Echo  (score: 0.98)
       - Energy 0.82 is close to target 0.80
  2. Rooftop Lights — Indigo Parade  (score: 0.96)
       - Energy 0.76 is close to target 0.80
  3. Night Drive Loop — Neon Echo  (score: 0.95)
       - Energy 0.75 is close to target 0.80

======================================================================
PROFILE: Missing genre key entirely
  prefs = {'mood': 'sad', 'energy': 0.9}
----------------------------------------------------------------------
  1. Storm Runner — Voltline  (score: 0.99)
       - Energy 0.91 is close to target 0.90
  2. Gym Hero — Max Pulse  (score: 0.97)
       - Energy 0.93 is close to target 0.90
  3. Sunrise City — Neon Echo  (score: 0.92)
       - Energy 0.82 is close to target 0.90

======================================================================
PROFILE: Unsupported mood value ('sad' not in catalog)
  prefs = {'genre': 'pop', 'mood': 'sad', 'energy': 0.8}
----------------------------------------------------------------------
  1. Sunrise City — Neon Echo  (score: 2.98)
       - Matches favorite genre 'pop'
       - Energy 0.82 is close to target 0.80
  2. Gym Hero — Max Pulse  (score: 2.87)
       - Matches favorite genre 'pop'
       - Energy 0.93 is close to target 0.80
  3. Rooftop Lights — Indigo Parade  (score: 0.96)
       - Energy 0.76 is close to target 0.80

======================================================================
PROFILE: No preferences match anything
  prefs = {'genre': 'metal', 'mood': 'furious', 'energy': 0.5}
----------------------------------------------------------------------
  1. Midnight Coding — LoRoom  (score: 0.92)
       - Energy 0.42 is close to target 0.50
  2. Focus Flow — LoRoom  (score: 0.90)
       - Energy 0.37 is close to target 0.50
  3. Coffee Shop Stories — Slow Stereo  (score: 0.87)
       - Energy 0.37 is close to target 0.50
```

**What I observed:**

- **Genre dominates conflicts, as designed.** In every conflicting profile, the genre-matching songs won even when their mood and energy were way off — e.g. the lofi/happy/0.9 user got three low-energy lofi tracks. This confirms the "genre over-prioritization" bias I predicted in the recipe.
- **Case sensitivity is a real bug.** `'POP'` / `'Happy'` matched nothing, so a user typing with capital letters silently loses their genre and mood signal and just gets energy-sorted results. The comparison should lowercase both sides.
- **Out-of-range energy doesn't break anything, but it distorts.** With `energy = 1.7`, the closeness score stays positive but rewards impossible targets (0.93 scores 0.23); with `energy = -0.5`, closeness can go negative. Inputs should be clamped to [0, 1].
- **Missing keys degrade gracefully.** With `energy = None` or no genre key, the system just skips that signal rather than crashing — the remaining signals still rank sensibly.
- **The system never returns "no results."** Even for a user whose preferences match nothing (metal/furious), it confidently ranks songs on energy alone. That's fine here, but in a real system you might want a confidence threshold or an explicit "weak match" flag.

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



