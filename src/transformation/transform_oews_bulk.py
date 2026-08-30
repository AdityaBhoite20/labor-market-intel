import pandas as pd
import numpy as np
import glob
import os

pd.set_option('future.no_silent_downcasting', True)

SUPPRESSION_CODES = ["#", "*", "**"]

def load_oews_year(year: int) -> pd.DataFrame:
    filepath = f"data/raw/bls_oews_bulk/oews_national_{year}.xlsx"
    df = pd.read_excel(filepath)

    df.columns = df.columns.str.upper()

    if "OCC_GROUP" in df.columns:
        df = df.rename(columns={"OCC_GROUP": "O_GROUP"})

    df_detailed = df[df["O_GROUP"] == "detailed"].copy()
    df_detailed["year"] = year
    return df_detailed

years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
all_years = [load_oews_year(y) for y in years]

combined = pd.concat(all_years, ignore_index=True)
print(combined.shape)
print(combined["year"].value_counts())

final_columns = combined[[
    "OCC_CODE", "OCC_TITLE", "year",
    "TOT_EMP", "A_MEDIAN", "A_MEAN",
    "A_PCT10", "A_PCT25", "A_PCT75", "A_PCT90"
]].copy()

final_columns = final_columns.rename(columns={
    "OCC_CODE": "soc_code",
    "OCC_TITLE": "occupation_title",
    "TOT_EMP": "employment",
    "A_MEDIAN": "median_wage",
    "A_MEAN": "mean_wage",
    "A_PCT10": "wage_pct10",
    "A_PCT25": "wage_pct25",
    "A_PCT75": "wage_pct75",
    "A_PCT90": "wage_pct90",
})

wage_columns = ["median_wage", "mean_wage", "wage_pct10", "wage_pct25", "wage_pct75", "wage_pct90"]

for col in wage_columns:
    final_columns[col] = final_columns[col].replace(SUPPRESSION_CODES, np.nan)
    final_columns[col] = pd.to_numeric(final_columns[col])

final_columns["employment"] = final_columns["employment"].replace(SUPPRESSION_CODES, np.nan)
final_columns["employment"] = pd.to_numeric(final_columns["employment"])

print(final_columns.dtypes)
print(final_columns.describe())

def save_processed(df: pd.DataFrame, filename: str, folder: str = "data/processed"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to: {filepath}")

save_processed(final_columns, "oews_all_occupations_2015_2025.csv")