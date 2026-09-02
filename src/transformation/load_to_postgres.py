import pandas as pd
import sys
sys.path.append("src/transformation")
from db_connection import get_db_engine

engine = get_db_engine()

curated_tables = {
    "oews_occupations": "oews_all_occupations_2015_2025.csv",
    "master_occupations": "master_occupations.csv",
    "occupation_clusters": "occupation_clusters.csv",
    "employment_forecast": "employment_forecast_2030_2035.csv",
    "forecast_vs_bls": "forecast_vs_bls_comparison.csv",
    "ai_exposure_scores": "ai_exposure_scores.csv",
    "ai_exposure_vs_growth": "ai_exposure_vs_growth.csv",
    "ces_industry_trends": "ces_industry_trends_clean.csv",
    "laus_state_trends": "laus_state_trends_clean.csv",
    "job_title_clusters": "job_title_clusters.csv",
    "skill_wage_analysis": "full_skill_wage_analysis.csv",
    "laus_all_states": "laus_all_states_2015_2025.csv",
}

for table_name, filename in curated_tables.items():
    df = pd.read_csv(f"data/curated/{filename}")
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Loaded {table_name} table ({len(df)} rows)")