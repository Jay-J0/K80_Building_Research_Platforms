#Script for receiving .xml data from Entsoe
#Transparency Platform Restful API documentation: https://documenter.getpostman.com/view/7009892/2s93JtP3F6#d4383852-1e53-4f98-a028-e0d9ac73d5f5
#Entsoe: https://transparency.entsoe.eu/dashboard/show
#Area Codes: https://transparencyplatform.zendesk.com/hc/en-us/articles/15885757676308-Area-List-with-Energy-Identification-Code-EIC
#entsoe-py project description: https://pypi.org/project/entsoe-py/ 
import requests
import pandas as pd
import os
import time
from entsoe import EntsoePandasClient

api_key = 'eb7ce115-9f12-468e-a744-930a6a104c79'

url = "https://web-api.tp.entsoe.eu/api"

countryCodesEU = [
    "AT",  # Austria
    "BE",  # Belgium
    "BG",  # Bulgaria
    "HR",  # Croatia
    "CY",  # Cyprus
    "CZ",  # Czech Republic
    "DK",  # Denmark
    "EE",  # Estonia
    "FI",  # Finland
    "FR",  # France
    "DE",  # Germany
    "GR",  # Greece
    "HU",  # Hungary
    "IE",  # Ireland
    "IT",  # Italy
    "LV",  # Latvia
    "LT",  # Lithuania
    "LU",  # Luxembourg
    "MT",  # Malta
    "NL",  # Netherlands
    "PL",  # Poland
    "PT",  # Portugal
    "RO",  # Romania
    "SK",  # Slovakia
    "SI",  # Slovenia
    "ES",  # Spain
    "SE"   # Sweden
]

#naming convention:
# NL2024.csv -> 2024-01-01 tot 2024-12-31 (of meest recente datum) voor nederland

start_year = 2015
end_year = 2026

for country in countryCodesEU:
    if country != "NL":
        continue

    for year in range (start_year, end_year):
        filename = f"{country}{year}.csv"
        if not os.path.exists(filename): #if we didn't scrape it yet...
            client = EntsoePandasClient(api_key=api_key)
            start = pd.Timestamp(f'{year}0101', tz='Europe/Brussels')
            end = pd.Timestamp(f'{year}1231', tz='Europe/Brussels')

            try:
                print(f"Opvragen: {country} - {year}")
                pd_dataframe = client.query_generation(country, start=start, end=end, psr_type=None)
                pd_dataframe.to_csv(filename, index=False)
                print(f"Opgeslagen als: {filename}")
                time.sleep(10)

            except Exception as e:
                print(f"Fout bij {country} - {year}: {e}")
        else:
            print(f"{country}{year} is al opgehaald, wordt dus overgeslagen")




print("Done!")