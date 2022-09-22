import requests
import json

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

parameters = {
    "start": 20210101,
    "end"  : 20210102,
    "latitude": 38.9573,
    "longitude": -75.4903,
    "community": "re",
    "parameters": "ALLSKY_SFC_LW_DWN"
}

response = requests.get("https://power.larc.nasa.gov/api/temporal/hourly/point", params = parameters)

print(response.status_code)
jprint(response.json())