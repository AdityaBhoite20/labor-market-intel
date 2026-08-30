import pandas as pd
import os

skills_full = pd.read_csv("data/raw/onet/db_31_0_csv/essential_skills.csv")
skills_full["soc_code_clean"] = skills_full["O*NET-SOC Code"].str.split(".", regex=False).str[0]

importance_only = skills_full[skills_full["Scale Name"] == "Importance"]
skills_clean_full = importance_only[["Title", "soc_code_clean", "Element Name", "Data Value"]]
skills_clean_full = skills_clean_full.rename(columns={
    "Title": "occupation_title",
    "Element Name": "skill_name",
    "Data Value": "importance_score"
})

print(skills_clean_full.shape)

oews_full = pd.read_csv("data/processed/oews_all_occupations_2020_2025.csv")
oews_2025 = oews_full[oews_full["year"] == 2025]

full_skill_wage = skills_clean_full.merge(
    oews_2025,
    left_on="soc_code_clean",
    right_on="soc_code",
    how="inner"
)

print(full_skill_wage.shape)

def save_processed(df: pd.DataFrame, filename: str, folder: str = "data/processed"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to: {filepath}")

save_processed(full_skill_wage, "full_skill_wage_analysis.csv")
