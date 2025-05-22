import pandas as pd
import os

country = "NL"
start_year = 2015
end_year = 2026  # exclusief

all_dfs = []

broken = False

for year in range(start_year, end_year):
    filename = f"{country}{year}.csv"
    if os.path.exists(filename):
        print(f"Laden: {filename}")
        if start_year == year:
            df = pd.read_csv(filename, index_col=None, skiprows=0)
        else:
            df = pd.read_csv(filename, index_col=None, skiprows=2)
        df['year'] = year  # optioneel: voeg kolom toe met jaartal
        all_dfs.append(df)
    else:
        print(f"Bestand ontbreekt: {filename}")
        broken = True
        break


#niet opslaan als het bestand jaren mist
if broken == False:
    # Combineer alles
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Opslaan
    combined_df.to_csv(f"{country}_all_years.csv", index=False)
    print(f"Samengevoegd bestand opgeslagen als: {country}_all_years.csv")
