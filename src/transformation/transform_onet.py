import os
import pandas as pd 
import sys
sys.path.append("src/ingestion")
from occupation_reference import OCCUPATIONS



occupations = pd.read_csv("data/raw/onet/db_31_0_csv/occupation_data.csv")
# print(occupations.head())
# print(occupations.shape)
target_soc_codes = [occ["soc_code"] for occ in OCCUPATIONS]

occupations["soc_code_clean"] = occupations["O*NET-SOC Code"].str.split(".",regex=False).str[0]

filtered_occupations = occupations[occupations["soc_code_clean"].isin(target_soc_codes)]
filtered_occupations = filtered_occupations.sort_values("O*NET-SOC Code")
filtered_occupations = filtered_occupations.drop_duplicates(subset="soc_code_clean",keep="first")
print(filtered_occupations)

skills = pd.read_csv("data/raw/onet/db_31_0_csv/essential_skills.csv")
skills["soc_code_clean"] = skills["O*NET-SOC Code"].str.split(".",regex=False).str[0]
filtered_skills = skills[skills["soc_code_clean"].isin(target_soc_codes)]
print(filtered_skills.shape)
print(filtered_skills.head(10))

importance_only = filtered_skills[filtered_skills["Scale Name"] == "Importance"]
skills_clean = importance_only[["Title", "soc_code_clean", "Element Name", "Data Value"]]
skills_clean = skills_clean.rename(columns={
    "Title": "occupation_title",
    "Element Name": "skill_name",
    "Data Value": "importance_score"
})
print(skills_clean.head(10))

def save_processed(df:pd.DataFrame, filename:str, folder:str ="data/processed"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Saved Processed data to: {filepath}")

save_processed(filtered_occupations,"onet_occupations.csv")
save_processed(skills_clean,"onet_skills.csv")
