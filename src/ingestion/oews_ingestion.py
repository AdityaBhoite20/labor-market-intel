import os 
import json
from datetime import datetime
from dotenv import load_dotenv
from bls_ingestion import fetch_bls_series, save_raw
from occupation_reference import OCCUPATIONS

load_dotenv()

DATATYPE_CODES = {
    "employment": "01",
    "annual_mean_wage": "04",
    "annual_median_wage": "13",
}

def build_oews_series_id(soc_code:str, datatype:str) ->str:
    occupation_code = soc_code.replace("-","")
    datatype_code = DATATYPE_CODES[datatype]

    series_id = (
        "OE"        # survey
        + "U"       # seasonal (always U for OEWS)
        + "N"       # area type: National
        + "0000000" # area code: national = 7 zeros
        + "000000"  # industry code: cross-industry
        + occupation_code  # 6-digit SOC, no hyphen
        + datatype_code    # 2-digit measure
    )
    return series_id


if __name__ == "__main__":
    all_series_ids = []
    series_lookup = {}

    for occupation in OCCUPATIONS:
        title = occupation["title"]
        soc_code = occupation["soc_code"]

        employment_id = build_oews_series_id(soc_code, "employment")
        median_wage_id = build_oews_series_id(soc_code, "annual_median_wage")

        all_series_ids.append(employment_id)
        all_series_ids.append(median_wage_id)

        series_lookup[employment_id] = f"{title} - Employment"
        series_lookup[median_wage_id] = f"{title} - Median Wage"

    print(f"Fetching {len(all_series_ids)} OEWS series...")
    data = fetch_bls_series(all_series_ids, "2025", "2025")
    save_raw(data, source="oews_occupations")

# if __name__ == "__main__":
#     test_series = build_oews_series_id("15-1252", "employment")

#     for year in ["2022", "2023", "2024"]:
#         print(f"\nTrying year: {year}")
#         try:
#             data = fetch_bls_series([test_series], year, year)
#             print("SUCCESS:", json.dumps(data["Results"], indent=2))
#         except ValueError as e:
#             print("Failed:", e)


# if __name__ == "__main__":
#     all_series_ids = []
#     series_lookup = {}

#     for occupation in OCCUPATIONS:
#         title = occupation["title"]
#         soc_code = occupation["soc_code"]

#         employment_id = build_oews_series_id(soc_code, "employment")
#         median_wage_id = build_oews_series_id(soc_code, "annual_median_wage")

#         all_series_ids.append(employment_id)
#         all_series_ids.append(median_wage_id)

#         series_lookup[employment_id] = f"{title} - Employment"
#         series_lookup[median_wage_id] = f"{title} - Median Wage"

#     print(f"Fetching {len(all_series_ids)} OEWS series...")
#     data = fetch_bls_series(all_series_ids, "2023", "2024")
#     save_raw(data, source="oews_occupations")


# if __name__ == "__main__":
#     test_id = build_oews_series_id("25-2021","annual_median_wage")
#     expected = "OEUS280000000000025201113"
#     fields = {
#         "survey":     (0, 2),
#         "seasonal":   (2, 3),
#         "areatype":   (3, 4),
#         "area_code":  (4, 11),
#         "industry":   (11, 17),
#         "occupation": (17, 23),
#         "datatype":   (23, 25),
#     }
#     print(f"{'Field':<12}{'Constructed':<15}{'Expected':<15}")
#     for field, (start,end) in fields.items():
#         print(f"{field:<12}{test_id[start:end]:<15}{expected[start:end]:<15}")