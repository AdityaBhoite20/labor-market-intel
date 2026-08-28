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

if __name__ == "__main__":
    data = fetch_bls_series(["LNS14000000"], "2023", "2024")
    save_raw(data, source="unemployment_rate")
# if __name__ == "__main__":
#     data = fetch_bls_series(["LNS14000000"], "2023", "2024")
#     print(json.dumps(data,indent=2))

