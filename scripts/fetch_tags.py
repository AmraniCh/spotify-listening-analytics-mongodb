import json
import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

SAMPLE_PATH = "data/processed/sample.csv"
CACHE_PATH = "data/processed/artist_tags.json"

SLEEP_SECONDS = 0.25
SAVE_EVERY = 50


def fetch_artist_tags(artist: str) -> list[str]:
    """Return the list of top tags for a given artist name."""
    params = {
        "method": "artist.getTopTags",
        "artist": artist,
        "api_key": API_KEY,
        "format": "json",
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        return []

    tags = data.get("toptags", {}).get("tag", [])
    return [tag["name"] for tag in tags]


def load_cache(path: str) -> dict:
    """Load previously fetched tags, or start empty."""
    if Path(path).exists():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict, path: str) -> None:
    """Write the cache to disk."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    df = pd.read_csv(SAMPLE_PATH)
    artists = df["artist_name"].unique()

    cache = load_cache(CACHE_PATH)
    todo = [a for a in artists if a not in cache]

    print(f"Artists in sample: {len(artists)}")
    print(f"Already cached: {len(cache)}")
    print(f"To fetch: {len(todo)}")

    for i, artist in enumerate(todo, start=1):
        print(i, artist)
        try:
            cache[artist] = fetch_artist_tags(artist)
        except Exception as exc:
            print(f"  [FAIL] {artist}: {exc}")
            cache[artist] = []

        if i % SAVE_EVERY == 0:
            save_cache(cache, CACHE_PATH)
            print(f"  {i}/{len(todo)} fetched")

        time.sleep(SLEEP_SECONDS)

    save_cache(cache, CACHE_PATH)

    empty = sum(1 for tags in cache.values() if not tags)
    print(f"\nDone. {len(cache)} artists cached.")
    print(f"Artists with no tags: {empty} ({empty / len(cache) * 100:.1f}%)")
