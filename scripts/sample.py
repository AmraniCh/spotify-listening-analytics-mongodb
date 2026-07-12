import pandas as pd

DATASET_PATH = "data/raw/spotify_history.csv"
OUTPUT_PATH = "data/processed/sample.csv"
START_DATE_FILTER = "2023-07-01"

df = pd.read_csv(DATASET_PATH)
df["ts"] = pd.to_datetime(df["ts"])

filtered = df[df["ts"] >= START_DATE_FILTER]
filtered = filtered.sort_values("ts", ascending=False).head(12000)

filtered.to_csv(OUTPUT_PATH, index=False)