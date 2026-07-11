import pandas as pd

RAW_PATH = "data/raw/spotify_history.csv"

def print_overview(df):
    print(f'Rows: {len(df)}')
    print(f"Oldest listen: {df['ts'].min()}")
    print(f"Most recent listen: {df['ts'].max()}")
    print(f'Columns: {df.columns.tolist()}')

if __name__ == "__main__":
    
    df = pd.read_csv(RAW_PATH)
    df["ts"] = pd.to_datetime(df["ts"])

    print_overview(df)