import os
import pandas as pd

def normalize_and_merge_csvs(directory, country_prefix, output_file):
    merged_data = []

    for filename in os.listdir(directory):
        if filename.startswith(country_prefix) and filename.endswith(".csv"):
            year = ''.join(filter(str.isdigit, filename))
            file_path = os.path.join(directory, filename)
            print(f"Processing: {filename}")

            df = pd.read_csv(file_path)

            # Separate columns into 'actual aggregated' and 'actual consumption'
            aggregated_cols = [col for col in df.columns if not col.endswith('.1')]
            consumption_cols = [col for col in df.columns if col.endswith('.1')]

            for col in aggregated_cols:
                source = col.strip()
                aggregated = df[col]
                consumption = df.get(f"{col}.1", pd.Series([None] * len(df)))  # Use NaNs if consumption is missing

                temp_df = pd.DataFrame({
                    'year': int(year),
                    'energy source': source,
                    'actual aggregated': aggregated,
                    'actual consumption': consumption
                })
                merged_data.append(temp_df)

    if merged_data:
        final_df = pd.concat(merged_data, ignore_index=True)
        final_df.to_csv(output_file, index=False)
        print(f"\n✅ Merged data saved to: {output_file}")
    else:
        print("⚠️ No valid files found to merge.")

# ==========================
# Example Usage
# ==========================
if __name__ == "__main__":
    # Customize these paths as needed
    input_folder = "./EntsoeData/France"     # Folder containing DK2015.csv, DK2016.csv, ...
    country_code = "FR"                # Country prefix in filenames
    output_csv = "merged_FR.csv"       # Output merged file

    normalize_and_merge_csvs(input_folder, country_code, output_csv)

