import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

demand = pd.read_excel('Delaware_Model_Data_2019.xlsx')
demand['monthyear']=pd.to_datetime(demand['datetime']).dt.strftime('%Y-%m')
print(demand.to_string())

demand.plot(x = 'Hours', y = 'Gas Usage [kWh]')


plt.title("Thermal Demand vs Hours for 2015-2019")
plt.xlabel("Hours")
plt.ylabel("Thermal Demand (kWh)")
plt.show()