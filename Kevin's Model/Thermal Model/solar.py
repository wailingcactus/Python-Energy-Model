import pandas as pd
import requests
import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get_solar(start, end, lat, long, area, efficiency):
    parameters = {
        "start": start,
        "end"  : end,
        "latitude": lat,
        "longitude": long,
        "community": "re",
        "parameters": "ALLSKY_SFC_SW_DWN",
        "time-standard": "lst"
    }

    response = requests.get("https://power.larc.nasa.gov/api/temporal/hourly/point", params = parameters)
    # print(response.status_code)
    #jprint(response.json())

    r = response.json()
    irradiance_dictionary = r['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    d = {'datetime':irradiance_dictionary.keys(), 'irradiance_Wh_m2':irradiance_dictionary.values()}
    solar = pd.DataFrame(d)

    #Calculate solar production based on irradiance, solar panel area, and efficiency
    area = area
    efficiency = efficiency
    solar['solar_production_kWh'] = solar['irradiance_Wh_m2']*efficiency*area/1000 # Take the irradiance and calculate solar production based on efficiency and panel area in kWh
    return solar