import import_demand
import geothermal_system
import solar
import matplotlib.pyplot as plt

#Constants
greenhouse_area = 100000 #m^2

# Demand Parameters
demand_file = 'Delaware_Model_Data_2018.xlsx'

# Solar Parameters
start_date = 20180101
end_date = 20181231
lat = 38.9573
long = -75.4903
solar_area = 0.2 * greenhouse_area
panel_efficiency = 0.2

# Importing yearly demand data

demand = import_demand.import_data(demand_file)
annual_heating = round(sum(demand['gas_usage_kWh']))
print(f"Annual thermal demand is {annual_heating} kWh")

# Calculate average thermal hourly demand, and size geothermal system.
average_heating = annual_heating/8760
geothermal_system = geothermal_system.geothermal_system(average_heating)
demand['geothermal_kWh'] = geothermal_system

# Pull in solar data
solar = solar.get_solar(start_date, end_date, lat, long, solar_area, panel_efficiency)
demand['solar_kWh'] = solar['solar_production_kWh']

# Plotting
demand.plot(y = ['gas_usage_kWh','geothermal_kWh','electricity_usage_kWh','solar_kWh'])
plt.show()