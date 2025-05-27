import pandas as pd
import glob
import os
import re

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

# Directory where the CSVs are located
csv_folder = "."

# Pattern to match all NL CSV files
csv_files = sorted(glob.glob(os.path.join(csv_folder, "NL*.csv")))

all_dfs = []

for file in csv_files:
    # Extract year from filename using regex
    match = re.search(r'NL(\d{4})\.csv', os.path.basename(file))
    if match:
        year = int(match.group(1))
    else:
        continue  # Skip files that don't match the pattern

    df = pd.read_csv(file)
    df["Year"] = year  # Add year column
    all_dfs.append(df)

# Combine all into one DataFrame
combined_df = pd.concat(all_dfs, ignore_index=True)

# Save to a new CSV file
combined_df.to_csv("NL_combined(2015-2025).csv", index=False)

print(f"Combined {len(csv_files)} files into 'NL_combined.csv' with a Year column.")
