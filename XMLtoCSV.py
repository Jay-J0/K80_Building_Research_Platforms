import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

# Mapping van productietypes
production_type_mapping = {
    "B01": "Biomass",
    "B02": "Fossil Brown coal/Lignite",
    "B03": "Fossil Coal-derived gas",
    "B04": "Fossil Gas",
    "B05": "Fossil Hard coal",
    "B06": "Fossil Oil",
    "B07": "Fossil Oil shale",
    "B08": "Fossil Peat",
    "B09": "Geothermal",
    "B10": "Hydro Pumped Storage",
    "B11": "Hydro Run-of-river and poundage",
    "B12": "Hydro Water Reservoir",
    "B13": "Marine",
    "B14": "Nuclear",
    "B15": "Other renewable",
    "B16": "Solar",
    "B17": "Waste",
    "B18": "Wind Offshore",
    "B19": "Wind Onshore",
    "B20": "Other",
    "B25": "Energy storage"
}

# XML-bestand openen
tree = ET.parse("EntsoeData.xml")
root = tree.getroot()

# De juiste namespace instellen
ns = {'ns': 'urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'}

rows = []

# Elk TimeSeries-blok parsen
for ts in root.findall('ns:TimeSeries', ns):
    raw_type = ts.find('ns:MktPSRType/ns:psrType', ns).text
    psr_type = production_type_mapping.get(raw_type, raw_type)
    period = ts.find('ns:Period', ns)
    resolution = period.find('ns:resolution', ns).text
    interval_start = period.find('ns:timeInterval/ns:start', ns).text
    interval_start_dt = datetime.fromisoformat(interval_start.replace('Z', '+00:00'))

    for point in period.findall('ns:Point', ns):
        position = int(point.find('ns:position', ns).text)
        quantity = float(point.find('ns:quantity', ns).text)

        # Bepaal tijdstip per punt
        if resolution == 'PT15M':
            timestamp = interval_start_dt + timedelta(minutes=15 * (position - 1))
        elif resolution == 'PT60M':
            timestamp = interval_start_dt + timedelta(hours=position - 1)
        else:
            timestamp = interval_start_dt  # fallback

        rows.append({
            'productionType': psr_type,
            'timestamp': timestamp,
            'quantity_MW': quantity
        })

# Dataframe maken van 15-minuten data
df = pd.DataFrame(rows)

# Nieuw: Per uur samenvatten
df['timestamp_hour'] = df['timestamp'].dt.floor('h')
#df_hourly = df.groupby(['productionType', 'timestamp_hour'])['quantity_MW'].sum().reset_index()
df_hourly = df.groupby(['productionType', 'timestamp_hour'], as_index=False)['quantity_MW'].sum()

# Opslaan
df.to_csv('./entsoe_data_raw.csv', index=False)          # Optioneel: ruwe 15-min data
df_hourly.to_csv('./entsoe_data_hourly.csv', index=False)  # Per uur samengevat

print("CSV-bestanden opgeslagen als 'entsoe_data_raw.csv' en 'entsoe_data_hourly.csv'")
