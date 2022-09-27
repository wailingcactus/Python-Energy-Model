import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import numpy as np

demand = pd.read_excel('Delaware_Model_Data_2019.xlsx')
demand['monthyear']=pd.to_datetime(demand['datetime']).dt.strftime('%Y-%m')
print(demand.to_string())


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

demand['Solar Production'] = irradiance[2]

ax = demand.plot(x = 'Hours', y = ['Gas Usage [kWh]','Electricity usage [kWh]', 'Solar Production'])

plt.title("Greenhouse Demand vs Hours for 2019")
plt.xlabel("Hours")
plt.ylabel("Energy (kWh)")
plt.show()


