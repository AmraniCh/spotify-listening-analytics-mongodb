import json
from pathlib import Path

import pandas as pd

SAMPLE_PATH = "data/processed/sample.csv"
GENRES_PATH = "data/processed/artist_genres.json"
OUTPUT_PATH = "data/processed/listens.json"

N_USERS = 4
UNKNOWN = "Unknown"


def assign_users(df: pd.DataFrame, n_users: int) -> pd.Series:
    chunk_size = len(df) // n_users
    user_index = pd.Series(df.index // chunk_size).clip(upper=n_users - 1)
    return "user_" + (user_index + 1).astype(str).str.zfill(2)


def build_document(row: dict, position: int) -> dict:
    return {
        "_id": f"eco_{position:05d}",
        "id_utilisateur": row["id_utilisateur"],
        "spotify_track_uri": row["spotify_track_uri"],
        "morceau": {
            "titre": row["track_name"],
            "artiste": row["artist_name"],
            "album": row["album_name"],
            "genre": row["genre"],
        },
        "plateforme": row["platform"],
        "ms_played": int(row["ms_played"]),
        "reason_start": row["reason_start"],
        "reason_end": row["reason_end"],
        "shuffle": bool(row["shuffle"]),
        "skipped": bool(row["skipped"]),
        "date_ecoute": {"$date": row["ts"].strftime("%Y-%m-%dT%H:%M:%SZ")},
    }


if __name__ == "__main__":
    df = pd.read_csv(SAMPLE_PATH)
    df["ts"] = pd.to_datetime(df["ts"])

    # chronological order drives both the user split and the _id sequence
    df = df.sort_values("ts").reset_index(drop=True)

    genre_map = json.loads(Path(GENRES_PATH).read_text(encoding="utf-8"))
    df["genre"] = df["artist_name"].map(genre_map).fillna(UNKNOWN)

    df["id_utilisateur"] = assign_users(df, N_USERS)

    df["reason_start"] = df["reason_start"].fillna("unknown")
    df["reason_end"] = df["reason_end"].fillna("unknown")

    documents = [
        build_document(row, position)
        for position, row in enumerate(df.to_dict("records"), start=1)
    ]

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_PATH).write_text(
        json.dumps(documents, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Documents built: {len(documents)}")
    print("\nListens per user:")
    print(df["id_utilisateur"].value_counts().sort_index().to_string())
    print(f"\nGenres: {df['genre'].nunique()}")
    print(f"Unknown genre: {(df['genre'] == UNKNOWN).sum()}")
    print(f"\nSaved to {OUTPUT_PATH}")