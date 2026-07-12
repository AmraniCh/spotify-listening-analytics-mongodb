"""Count tag frequency across all artists to derive the genre whitelist.

Reads the cache built by 03a. Makes no API calls.
"""

import json
from collections import Counter
from pathlib import Path

CACHE_PATH = "data/processed/artist_tags.json"
TOP_N = 60


if __name__ == "__main__":
    cache = json.loads(Path(CACHE_PATH).read_text(encoding="utf-8"))

    counter = Counter()
    for tags in cache.values():
        for tag in tags:
            counter[tag.lower()] += 1

    print(f"Artists: {len(cache)}")
    print(f"Distinct tags: {len(counter)}\n")

    print(f"Top {TOP_N} tags:\n")
    for rank, (tag, count) in enumerate(counter.most_common(TOP_N), start=1):
        print(f"{rank:3}. {tag:<30} {count:>5}")
