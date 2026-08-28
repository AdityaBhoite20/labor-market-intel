import json
import os
import glob
import pandas as pd
import sys
sys.path.append("src/ingestion")
from oews_ingestion import build_series_lookup

def get_latest_raw_file(pattern:str) -> str:
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No files matched pattern: {pattern}")
    return max(files, key=os.path.getctime)


def flatten_oews_data(raw_data: dict, lookup: dict) -> pd.DataFrame:
    rows = []

    for series in raw_data["Results"]["series"]:
        series_id = series["seriesID"]
        info = lookup.get(series_id)

        if info is None:
            print(f"WARNING: no lookup entry for series {series_id}, skipping")
            continue

        for record in series["data"]:
            rows.append({
                "occupation_title": info["title"],
                "soc_code": info["soc_code"],
                "measure": info["measure"],
                "year": record["year"],
                "value": record["value"],
            })

    return pd.DataFrame(rows)


def pivot_oews_data(df: pd.DataFrame) -> pd.DataFrame:
    pivoted = df.pivot_table(
        index=["occupation_title", "soc_code", "year"],
        columns="measure",
        values="value",
        aggfunc="first"
    ).reset_index()

    pivoted.columns.name = None
    return pivoted


def save_processed(df: pd.DataFrame, filename: str, folder: str = "data/processed"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to: {filepath}")

if __name__ == "__main__":
    latest_file = get_latest_raw_file("data/raw/bls/oews_occupations_*.json")
    print("Using file:", latest_file)

    with open(latest_file, "r") as f:
        raw_data = json.load(f)

    lookup = build_series_lookup()
    df = flatten_oews_data(raw_data, lookup)
    df_wide = pivot_oews_data(df)

    save_processed(df_wide, "oews_occupations.csv")