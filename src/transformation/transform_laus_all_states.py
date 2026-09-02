import pandas as pd
import numpy as np
import os
import shutil
shutil.copy("data/processed/laus_all_states_2015_2025.csv", "data/curated/laus_all_states_2015_2025.csv")

raw = pd.read_excel("data/raw/bls_laus_bulk/ststdsadata.xlsx", header=None, skiprows=8)

raw.columns = [
    "fips_code", "state", "year", "month",
    "civilian_pop", "labor_force", "labor_force_pct",
    "employment", "employment_pct", "unemployment_level", "unemployment_rate"
]

raw = raw.dropna(subset=["state", "year"])

raw["state"] = raw["state"].astype(str).str.strip()

us_states = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota",
    "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
    "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

laus_states_only = raw[raw["state"].isin(us_states)].copy()

laus_states_only["year"] = pd.to_numeric(laus_states_only["year"], errors="coerce")
laus_recent = laus_states_only[laus_states_only["year"] >= 2015].copy()

laus_final = laus_recent[["state", "year", "month", "unemployment_rate", "employment", "labor_force"]].copy()
laus_final["unemployment_rate"] = pd.to_numeric(laus_final["unemployment_rate"], errors="coerce")
laus_final["employment"] = pd.to_numeric(laus_final["employment"], errors="coerce")
laus_final["labor_force"] = pd.to_numeric(laus_final["labor_force"], errors="coerce")

print("Rows with invalid unemployment_rate after conversion:", laus_final["unemployment_rate"].isna().sum())

print(laus_final.shape)
print(laus_final["state"].nunique())
print(laus_final.head(10))

def save_processed(df: pd.DataFrame, filename: str, folder: str = "data/processed"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to: {filepath}")

save_processed(laus_final, "laus_all_states_2015_2025.csv")

shutil.copy("data/processed/laus_all_states_2015_2025.csv", "data/curated/laus_all_states_2015_2025.csv")

