import pandas as pd
import os

oews = pd.read_csv("data/processed/oews_occupations.csv")
onet = pd.read_csv("data/processed/onet_occupations.csv")

# print(oews.columns.tolist())
# print(onet.columns.tolist())

master = oews.merge(onet, left_on="soc_code", right_on="soc_code_clean",how="inner")

# print(master.shape)
# print(master.columns.tolist())

master_clean = master[["occupation_title", "soc_code", "year", "employment", "median_wage", "Description"]]
print(master_clean)

def save_processed(df: pd.DataFrame, filename:str, folder:str="data/processed"):
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    df.to_csv(filepath, index=False)
    print(f"Save processed data to: {filepath}")

save_processed(master_clean, "master_ocupations.csv")
