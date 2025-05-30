import os
import pandas as pd
import re

# Country code to name mapping
country_names = {
    "AT": "Austria",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "CY": "Cyprus",
    "CZ": "Czech_Republic",
    "DK": "Denmark",
    "EE": "Estonia",
    "FI": "Finland",
    "FR": "France",
    "DE": "Germany",
    "GR": "Greece",
    "HU": "Hungary",
    "IE": "Ireland",
    "IT": "Italy",
    "LV": "Latvia",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "MT": "Malta",
    "NL": "Netherlands",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "ES": "Spain",
    "SE": "Sweden"
}


input_dir = "EntsoeData"
output_dir = "CombinedData"
os.makedirs(output_dir, exist_ok=True)

for country_folder in os.listdir(input_dir):
    country_path = os.path.join(input_dir, country_folder)
    if os.path.isdir(country_path):
        all_data = []
        country_code = None

        for file in os.listdir(country_path):
            if file.endswith(".csv"):
                match = re.search(r'([A-Z]{2})(\d{4})\.csv', file)
                if match:
                    country_code = match.group(1)
                    year = match.group(2)
                    file_path = os.path.join(country_path, file)
                    try:
                        df = pd.read_csv(file_path)
                        df["Year"] = int(year)
                        all_data.append(df)
                    except Exception as e:
                        print(f"Failed to read {file_path}: {e}")

        if all_data and country_code:
            combined_df = pd.concat(all_data, ignore_index=True)
            country_name = country_names.get(country_code, country_folder)
            output_filename = os.path.join(output_dir, f"{country_name}_combined.csv")
            combined_df.to_csv(output_filename, index=False)
            print(f"Saved: {output_filename}")
        else:
            print(f"No data found or invalid code in: {country_folder}")
