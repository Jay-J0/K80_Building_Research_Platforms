import os
import pandas as pd

# Root directory with country subfolders
root_dir = "EntsoeData"

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


# Prepare list to store each DataFrame
combined_data = []

# Loop over each country folder
for country_folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, country_folder)
    
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                file_path = os.path.join(folder_path, file)

                try:
                    # Extract country code and year from filename like "NL2015.csv"
                    country_code = file[:2]
                    year = int(file[2:6])
                    country_name = country_names.get(country_code, country_code)

                    # Load CSV
                    df = pd.read_csv(file_path, low_memory=False)

                    # Add columns
                    df["Country"] = country_name
                    df["Year"] = year

                    combined_data.append(df)
                    print(f"Loaded {file}")

                except Exception as e:
                    print(f"Error processing {file}: {e}")

# Combine and save
if combined_data:
    combined_df = pd.concat(combined_data, ignore_index=True)
    combined_df.to_csv("entsoe_combined.csv", index=False)
    print("Combined CSV saved as 'entsoe_combined.csv'")
else:
    print("No data found.")


