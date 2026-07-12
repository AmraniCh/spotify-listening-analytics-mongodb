import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")


API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

ARTIST = "The Beatles"

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
        raise RuntimeError(f"Last.fm error {data['error']}: {data.get('message')}")

    tags = data.get("toptags", {}).get("tag", [])
    return [tag["name"] for tag in tags]


if __name__ == "__main__":
    tags = fetch_artist_tags(ARTIST)

    print(f"Artist: {ARTIST}")
    print(f"Tags found: {len(tags)}")
    for tag in tags[:10]:
        print(f"  - {tag}")