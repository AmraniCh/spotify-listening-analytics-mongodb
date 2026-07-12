import json
from pathlib import Path

import pandas as pd

SAMPLE_PATH = "data/processed/sample.csv"
CACHE_PATH = "data/processed/artist_tags.json"
OUTPUT_PATH = "data/processed/artist_genres.json"

UNKNOWN = "Unknown"

GENRE_WHITELIST = [
    "rock", "pop", "indie", "alternative", "singer-songwriter",
    "folk", "latin", "electronic", "soul", "funk", "jazz", "blues",
    "dance", "rnb", "hip-hop", "country", "rap", "psychedelic",
    "disco", "synthpop", "house", "punk", "classical", "experimental",
]

GENRE_ALIASES = {
    "hip hop": "hip-hop",
}

def match_genre(tags: list[str]) -> str:
    """Return the first tag matching the whitelist, or Unknown."""
    for tag in tags:
        normalized = tag.lower().strip()
        normalized = GENRE_ALIASES.get(normalized, normalized)

        if normalized in GENRE_WHITELIST:
            return normalized

    return UNKNOWN


def build_genre_map(cache: dict) -> dict:
    """Map every cached artist to a single genre."""
    return {artist: match_genre(tags) for artist, tags in cache.items()}


if __name__ == "__main__":
    cache = json.loads(Path(CACHE_PATH).read_text(encoding="utf-8"))
    genre_map = build_genre_map(cache)

    Path(OUTPUT_PATH).write_text(
        json.dumps(genre_map, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Coverage by artist
    unknown_artists = sum(1 for g in genre_map.values() if g == UNKNOWN)
    print(f"Artists: {len(genre_map)}")
    print(f"Unknown: {unknown_artists} ({unknown_artists / len(genre_map) * 100:.1f}%)")

    # Coverage by listen — the metric that actually matters
    df = pd.read_csv(SAMPLE_PATH)
    df["genre"] = df["artist_name"].map(genre_map).fillna(UNKNOWN)

    unknown_listens = (df["genre"] == UNKNOWN).sum()
    print(f"\nListens: {len(df)}")
    print(f"Unknown: {unknown_listens} ({unknown_listens / len(df) * 100:.1f}%)")

    # Genre distribution
    print("\nListens per genre:")
    print((df["genre"].value_counts(normalize=True) * 100).round(1).to_string())

    # Biggest artists we failed to classify
    print("\nTop unclassified artists:")
    unknown_df = df[df["genre"] == UNKNOWN]
    print(unknown_df["artist_name"].value_counts().head(20).to_string())