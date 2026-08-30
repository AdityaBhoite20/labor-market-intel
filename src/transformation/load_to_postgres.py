import pandas as pd
import sys
sys.path.append("src/transformation")
from db_connection import get_db_engine

engine = get_db_engine()

oews = pd.read_csv("data/processed/oews_all_occupations_2015_2025.csv")
oews.to_sql("oews_occupations", engine, if_exists="replace", index=False)
print("Loaded oews_occupations table")

master = pd.read_csv("data/processed/master_occupations.csv")
master.to_sql("master_occupations", engine, if_exists="replace", index=False)
print("Loaded master_occupations table")

onet_skills = pd.read_csv("data/processed/onet_skills.csv")
onet_skills.to_sql("onet_skills", engine, if_exists="replace", index=False)
print("Loaded onet_skills table")

ces = pd.read_csv("data/processed/ces_industry_trends_clean.csv")
ces.to_sql("ces_industry_trends", engine, if_exists="replace", index=False)
print("Loaded ces_industry_trends table")

laus = pd.read_csv("data/processed/laus_state_trends_clean.csv")
laus.to_sql("laus_state_trends", engine, if_exists="replace", index=False)
print("Loaded laus_state_trends table")

ai_exposure = pd.read_csv("data/processed/ai_exposure_scores.csv")
ai_exposure.to_sql("ai_exposure_scores", engine, if_exists="replace", index=False)
print("Loaded ai_exposure_scores table")

growth = pd.read_csv("data/processed/occupation_growth_2020_2025.csv")
growth.to_sql("occupation_growth", engine, if_exists="replace", index=False)
print("Loaded occupation_growth table")