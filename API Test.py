import pandas as pd
import requests
import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

parameters = {
    "start": 20190101,
    "end"  : 20191231,
    "latitude": 38.9573,
    "longitude": -75.4903,
    "community": "re",
    "parameters": "ALLSKY_SFC_SW_DWN",
    "time-standard": "utc"
}

response = requests.get("https://power.larc.nasa.gov/api/temporal/hourly/point", params = parameters)

efficiency = 0.2
area = 10000

print(response.status_code)
jprint(response.json())

r = response.json()
irradiance_dictionary = r['properties']['parameter']['ALLSKY_SFC_SW_DWN']
irradiance = pd.DataFrame(irradiance_dictionary.items())
irradiance[2] = irradiance [1]*efficiency*area/1000 # Take the irradiance and calculate solar production based on efficiency and panel area in kWh
