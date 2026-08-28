import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv


load_dotenv() #read .env file & loads key-value pairs

BLS_API_KEY = os.getenv("BLS_API_KEY")
BLS_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

def fetch_bls_series(series_ids: list[str], start_year:str, end_year:str) -> dict:
    payload = {
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year,
        "registrationkey": BLS_API_KEY,
    }
    response = requests.post(BLS_URL, json=payload)
    response.raise_for_status()
    return response.json()

def save_raw(data: dict, source:str, folder:str = "data/raw/bls"):
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{source}_{timestamp}.json"
    filepath = os.path.join(folder,filename)

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved raw data to: {filepath}")


SERIES_CONFIG = {
    "ces_industry_employment": [
        "CES0000000001",  # Total Nonfarm
        "CES6000000001",  # Professional & Business Services
        "CES6500000001",  # Education & Health Services
        "CES5000000001",  # Information
        "CES3000000001",  # Manufacturing
    ],
    "laus_state_unemployment": [
        "LASST060000000000003",  # California
        "LASST360000000000003",  # New York
        "LASST480000000000003",  # Texas
        "LASST170000000000003",  # Illinois
        "LASST120000000000003",  # Florida
    ],
}


if __name__ == "__main__":
    for source_name, series_ids in SERIES_CONFIG.items():
        print(f"Fetching: {source_name}")
        data = fetch_bls_series(series_ids,"2023","2024")
        save_raw(data, source=source_name)

# if __name__ == "__main__":
#     data = fetch_bls_series(["LNS14000000"], "2023", "2024")
#     print(json.dumps(data,indent=2))

