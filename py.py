#Script for clean data from IRENA
#https://pxweb.irena.org/pxweb/en/IRENASTAT/IRENASTAT__Power%20Capacity%20and%20Generation/

import pandas as pd
import os

europeanCountries = [
    'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium',
    'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
    'Denmark', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece',
    'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia',
    'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco',
    'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal',
    'Romania', 'Russia', 'San Marino', 'Serbia', 'Slovakia', 'Slovenia', 'Spain',
    'Sweden', 'Switzerland', 'Türkiye', 'Ukraine', 'United Kingdom', 'Vatican City'
]

euMemberStates = [
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
    'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
    'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
    'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
    'Spain', 'Sweden'
]


folder_path = "./csv/"
combinedEuroCountries_df = pd.DataFrame()
combinedEUMemberStates_df = pd.DataFrame()
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        print(file_path)
        temp_df = pd.read_csv(file_path, sep=";", encoding='ISO-8859-1', skiprows=2)

        filteredEuroCountries_df = temp_df[temp_df['Country/area'].isin(europeanCountries)]
        #print(filteredEuroCountries_df.head())

        filteredEUMemberStates_df = temp_df[temp_df['Country/area'].isin(euMemberStates)]
        #print(filteredEUMemberStates_df.head())


        
        combinedEuroCountries_df = pd.concat([combinedEuroCountries_df, filteredEuroCountries_df], ignore_index = True)
        combinedEUMemberStates_df = pd.concat([combinedEUMemberStates_df, filteredEUMemberStates_df], ignore_index = True)

combinedEuroCountries_df.to_csv("./EuropeanCountries.csv", index=False, encoding='utf-8')
combinedEUMemberStates_df.to_csv("./EUMemberStates.csv", index=False, encoding='utf-8')


