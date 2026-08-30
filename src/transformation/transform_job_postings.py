import pandas as pd
import os
import sys
sys.path.append("src/ingestion")

postings = pd.read_csv("data/raw/kaggle_job_postings/job_postings.csv")
skills = pd.read_csv("data/raw/kaggle_job_postings/job_skills.csv")

us_postings = postings[postings["search_country"] == "United States"]

combined = us_postings.merge(skills, on="job_link", how="inner")

def find_related_postings(df:pd.DataFrame, keyword:str) -> pd.DataFrame:
    mask = df["job_title"].str.contains(keyword, case=False, na=False)
    return df[mask]



OCCUPATION_KEYWORDS = {
    "Software Developers": "software developer",
    "Data Scientists": "data scientist",
    "Data Entry Keyers": "data entry",
    "Registered Nurses": "registered nurse",
    "Customer Service Representatives": "customer service",
    "Accountants and Auditors": "accountant",
    "Heavy and Tractor-Trailer Truck Drivers": "truck driver",
    "Market Research Analysts and Marketing Specialists": "market research",
    "Retail Salespersons": "retail sales",
    "Human Resources Specialists": "human resources",
}

def get_top_skills_for_occupation(df: pd.DataFrame, keyword: str, top_n: int = 10) -> pd.Series:
    matched = find_related_postings(df, keyword)
    skills_flat = matched["job_skills"].dropna().str.split(", ").explode()
    skills_clean = skills_flat.str.strip().str.title()
    return skills_clean.value_counts().head(top_n)

for occupation, keyword in OCCUPATION_KEYWORDS.items():
    print(f"\n=== {occupation} (keyword: '{keyword}') ===")
    top_skills = get_top_skills_for_occupation(combined, keyword)
    print(top_skills)



# data_scientist_postings = find_related_postings(combined,"data scientist")

# all_skills = data_scientist_postings["job_skills"].dropna().str.split(", ")
# all_skills_flat = all_skills.explode()

# all_skills_flat_clean = all_skills_flat.str.strip().str.title()
# skill_counts_clean = all_skills_flat_clean.value_counts()

# print(skill_counts_clean.head(20))

