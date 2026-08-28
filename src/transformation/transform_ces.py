import json
import os
import glob
import pandas as pd

def get_latest_raw_file(pattern: str) -> str:
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No files matched pattern: {pattern}")
    return max(files, key=os.path.getctime)

CES_LABELS = {
    "CES0000000001": "Total Nonfarm",
    "CES6000000001": "Professional & Business Services",
    "CES6500000001": "Education & Health Services",
    "CES5000000001": "Information",
    "CES3000000001": "Manufacturing",
}

def flatten_ces_data(raw_data: dict, labels: dict) -> pd.DataFrame:
    rows = []

    for series in raw_data["Results"]["series"]:
        series_id = series["seriesID"]
        industry_name = labels.get(series_id, "UNKNOWN")

        for record in series["data"]:
            rows.append({
                "industry": industry_name,
                "series_id": series_id,
                "year": record["year"],
                "period": record["periodName"],
                "employment_thousands": record["value"],
            })

    return pd.DataFrame(rows)

def save_processed(df: pd.DataFrame, filename: str, folder: str = "data/processed"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to: {filepath}")


if __name__ == "__main__":
    latest_file = get_latest_raw_file("data/raw/bls/ces_industry_employment_*.json")
    print("Using file:", latest_file)

    with open(latest_file, "r") as f:
        raw_data = json.load(f)

    df = flatten_ces_data(raw_data, CES_LABELS)
    save_processed(df, "ces_industry_employment.csv")
