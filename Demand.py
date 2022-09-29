import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import statistics

import numpy as np

demand = pd.read_excel('Delaware_Model_Data_2018.xlsx')
demand['monthyear']=pd.to_datetime(demand['datetime']).dt.strftime('%Y-%m')
print(demand.to_string())


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

parameters = {
    "start": 20180101,
    "end"  : 20181231,
    "latitude": 38.737088,
    "longitude": -75.600636,
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

demand['Solar Production'] = irradiance[2]
demand['Mismatch'] = demand['Electricity usage [kWh]'] - irradiance[2]

ax = demand.plot(x = 'datetime', y = ['Electricity usage [kWh]', 'Solar Production', 'Mismatch'])

plt.title("Greenhouse Demand vs Hours for 2019")
plt.xlabel("Hours")
plt.ylabel("Energy (kWh)")
plt.show()

excess = 0
for difference in demand['Mismatch']:
    if difference < 0:
        excess += difference

print(f"Excess energy is {excess} kWh")


