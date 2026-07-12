import pandas as pd

RAW_PATH = "data/raw/spotify_history.csv"

def print_overview(df: pd.DataFrame):
    print(f'Rows: {len(df)}')
    print(f"Oldest listen: {df['ts'].min()}")
    print(f"Most recent listen: {df['ts'].max()}")
    print(f'Columns: {df.columns.tolist()}')

def print_missing(df: pd.DataFrame):
    print(df.isnull().sum())

def print_cardinality(df: pd.DataFrame):
    print(f"Unique tracks: {df['spotify_track_uri'].nunique()}")
    print(f"Unique artists: {df['artist_name'].nunique()}")
    print(f"Unique albums: {df['album_name'].nunique()}")

def print_platforms(df: pd.DataFrame):
    print((df["platform"].value_counts(normalize=True) * 100).round(1))

def print_yearly(df: pd.DataFrame):
    print(df["ts"].dt.year.value_counts().sort_index())

def print_behavior(df: pd.DataFrame):
    print((df["skipped"].value_counts(normalize=True)).round(1))
    print()
    print((df["shuffle"].value_counts(normalize=True)).round(1))

def section(title: str):
    print(f"\n{'=' * 50}")
    print(title)
    print("=" * 50)
    
if __name__ == "__main__":
    
    df = pd.read_csv(RAW_PATH)
    df["ts"] = pd.to_datetime(df["ts"])

    section('Overview')
    print_overview(df)

    section('Missing values')
    print_missing(df)

    section('Cardinality')
    print_cardinality(df)

    section('Platforms')
    print_platforms(df)
    
    section('Listens per year')
    print_yearly(df)

    section('Behavior (Skip/Shuffle)')
    print_behavior(df)
    