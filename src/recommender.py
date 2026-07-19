import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0

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
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score, highest first."""
        scored = [(self._score(user, song), song) for song in self.songs]
        scored.sort(key=lambda pair: pair[0][0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable, semicolon-joined explanation for a song's score."""
        _, reasons = self._score(user, song)
        return "; ".join(reasons) if reasons else "No strong matches with your taste profile."

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Compute a weighted match score and the reasons behind it for one song."""
        score = 0.0
        reasons: List[str] = []

        if song.genre == user.favorite_genre:
            score += GENRE_WEIGHT
            reasons.append(f"Matches your favorite genre '{user.favorite_genre}'")

        if song.mood == user.favorite_mood:
            score += MOOD_WEIGHT
            reasons.append(f"Matches your preferred mood '{user.favorite_mood}'")

        energy_closeness = max(0.0, 1 - abs(song.energy - user.target_energy))
        score += energy_closeness * ENERGY_WEIGHT
        reasons.append(f"Energy {song.energy:.2f} is close to your target {user.target_energy:.2f}")

        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 0.5
            reasons.append("Acoustic sound matches your preference")

        return score, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_WEIGHT
        reasons.append(f"Matches favorite genre '{user_prefs.get('genre')}'")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_WEIGHT
        reasons.append(f"Matches preferred mood '{user_prefs.get('mood')}'")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_closeness = max(0.0, 1 - abs(song["energy"] - target_energy))
        score += energy_closeness * ENERGY_WEIGHT
        reasons.append(f"Energy {song['energy']:.2f} is close to target {target_energy:.2f}")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda item: item[1], reverse=True)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in scored[:k]]
