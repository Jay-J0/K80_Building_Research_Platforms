#Script for receiving .xml data from Entsoe
#Transparency Platform Restful API documentation: https://documenter.getpostman.com/view/7009892/2s93JtP3F6#d4383852-1e53-4f98-a028-e0d9ac73d5f5
#Entsoe: https://transparency.entsoe.eu/dashboard/show
import requests

api_key = 'eb7ce115-9f12-468e-a744-930a6a104c79'


url = "https://web-api.tp.entsoe.eu/api"


params = {
    'securityToken': api_key,
    'documentType': 'A75',         # Actual Generation per Production Type
    'processType': 'A16',          # Realized
    'in_Domain': '10Y1001A1001A83F',  # Example: Germany
    'periodStart': '202301010000',   # Start date (UTC)
    'periodEnd': '202301010100'      # End date (UTC)
}

response = requests.get(url, params=params)

print(f"Status Code: {response.status_code}")

print(response.text)
with open("kaas.xml", 'w') as f:
    f.write(response.text)