import pandas as pd
import os
import glob
import re

# Path setup
folder_path_in = './EntsoeData/'
output_file_out = '_combined_monthly_energy_data.csv'

# Find all CSV files starting with "NL"

countries_with_one_dinges = []

def process_country(folder_path, output_file):
    global countries_with_one_dinges
    all_data = []
    pattern = re.compile(r'^[A-Z]{2}\d{4}\.csv$')
    files = [f for f in os.listdir(folder_path) if pattern.match(f)]
    print("Found files:", files)

    if not files:
        print("No files found.")
        return

    # Process each file
    for file in files:
        file_path = os.path.join(folder_path, file)
        # Read first two rows to check for dual headers
        preview = pd.read_csv(file_path, nrows=2, header=None)
        first_row = preview.iloc[0]
        second_row = preview.iloc[1]

        # Check if second row has any non-numeric values → likely a second header
        has_second_header = any(pd.to_numeric(second_row, errors='coerce').isna())

        if has_second_header:
            df = pd.read_csv(file_path, skiprows=2, header=None)
            df.columns = pd.read_csv(file_path, low_memory=False).columns
        else:
            df = pd.read_csv(file_path, low_memory=False)


        filename = os.path.basename(file_path)

        # Extract year from filename (e.g., 'NL2015.csv')
        try:
            year = int(filename[2:6])
        except ValueError:
            print(f"Skipping {file_path}: couldn't extract year.")
            continue

        # Create timestamp column assuming 15-minute intervals starting Jan 1
        try:
            cc = filename[0:2]

            l = len(df)

            if 35040-100 <= l <= 35040+100:
                frequency = "15min"
            elif 17520-50 <= l <= 17520+50:
                frequency = "30min"
            elif 8760-25 <= l <= 8760+25:
                frequency = "1h"
            else:
                frequency = "1h"
                print(f"frequency klopt niet, {l} datapunten per jaar")


            print(f"frequency: {frequency}")
            start_time = pd.Timestamp(f"{year}-01-01 00:00")
            df['timestamp'] = pd.date_range(start=start_time, periods=len(df), freq=frequency)
            df.to_csv(str(os.path.join(folder_path, cc)) + "kaas.csv")
        except Exception as e:
            print(f"Failed to generate timestamps for {file_path}: {e}")
            continue

        # Extract month from timestamp
        df['month'] = df['timestamp'].dt.month

        # Process each energy source pair
        for col in df.columns:
            #print(col)
            if '.1' not in col and col not in ['timestamp', 'month']:
                prod_col = col
                cons_col = f"{col}.1"

                if cons_col in df.columns:
                    #print(f"now in year {year} month {df['month']}")
                    temp_df = pd.DataFrame({
                        'year': year,
                        'month': df['month'],
                        'electricity source': prod_col,
                        'electricity production MW': pd.to_numeric(df[prod_col], errors='coerce'),
                        'electricity consumption MW': pd.to_numeric(df[cons_col], errors='coerce')
                    })
                    
                    
                else:
                    #print(f"now in year {year} month {df['month']}")
                    if cc not in countries_with_one_dinges:
                        countries_with_one_dinges.append(cc)
                    temp_df = pd.DataFrame({
                        'year': year,
                        'month': df['month'],
                        'electricity source': prod_col,
                        'electricity consumption MW': pd.to_numeric(df[prod_col], errors='coerce')
                    })

                grouped = temp_df.groupby(['year', 'month', 'electricity source'], as_index=False).sum()
                #if 'electricity production MW' in grouped.columns:
                #    grouped['electricity production MW'] = grouped['electricity production MW'].astype(str) + ' MW'
                #grouped['electricity consumption MW'] = grouped['electricity consumption MW'].astype(str) + ' MW'
                
                
                all_data.append(grouped)
                
                
    try:
        os.remove(os.path.join(folder_path, cc + output_file))
    except FileNotFoundError:
        pass

    if not all_data:
        print("No valid data found to combine.")
        exit()

    # Combine all grouped data
    final_df = pd.concat(all_data, ignore_index=True)
    #final_df = final_df.groupby(['year', 'month', 'energy source'], as_index=False).sum()

    # Convert numeric month to full month name
    final_df['month'] = final_df['month'].apply(lambda x: pd.to_datetime(f'2023-{x:02d}-01').strftime('%B'))

    # Optional: Sort by year and calendar month order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
    final_df['month'] = pd.Categorical(final_df['month'], categories=month_order, ordered=True)
    final_df = final_df.sort_values(by=['year', 'month', 'electricity source'])

    # Save to CSV
    final_df.to_csv(os.path.join(folder_path, cc + output_file), index=False)
    print(f"Monthly aggregated file saved to {os.path.join(folder_path, cc + output_file)}")


for entry in os.listdir(folder_path_in):
    print(entry)

for entry in os.listdir(folder_path_in):
    full_path = os.path.join(folder_path_in, entry)
    if os.path.isdir(full_path):
        print(full_path)
        process_country(full_path, output_file_out)

print("landen met maar eeeeen waarde:")
print(countries_with_one_dinges)