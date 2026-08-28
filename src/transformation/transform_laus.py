import json
import os
import glob
import pandas as pd

def get_latest_raw_file(pattern: str) -> str:
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No files matched pattern: {pattern}")
    return max(files, key=os.path.getctime)


LAUS_LABELS = {
    "LASST060000000000003": "California",
    "LASST360000000000003": "New York",
    "LASST480000000000003": "Texas",
    "LASST170000000000003": "Illinois",
    "LASST120000000000003": "Florida",
}

def flatten_laus_data(raw_data: dict, labels: dict) -> pd.DataFrame:
    rows = []

    for series in raw_data["Results"]["series"]:
        series_id = series["seriesID"]
        state_name = labels.get(series_id, "UNKNOWN")

        for record in series["data"]:
            rows.append({
                "state": state_name,
                "series_id": series_id,
                "year": record["year"],
                "period": record["periodName"],
                "unemployment_rate": record["value"],
            })

    return pd.DataFrame(rows)

def save_processed(df: pd.DataFrame, filename: str, folder: str = "data/processed"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to: {filepath}")


if __name__ == "__main__":
    latest_file = get_latest_raw_file("data/raw/bls/laus_state_unemployment_*.json")
    print("Using file:", latest_file)

    with open(latest_file, "r") as f:
        raw_data = json.load(f)

    df = flatten_laus_data(raw_data, LAUS_LABELS)
    save_processed(df, "laus_state_unemployment.csv")
    print(df.head(10))