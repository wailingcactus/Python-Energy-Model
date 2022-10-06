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

# Importing yearly demand data and calculating statistics

hourly_demand = import_demand.import_data(demand_file)
daily_demand = hourly_demand.set_index(hourly_demand.index//24).sum(level=0) #Convert yearly demand to daily demand
annual_heating = round(sum(hourly_demand['gas_usage_kWh']))
annual_electricity = round(sum(hourly_demand['electricity_usage_kWh']))
baseload_heating = round(min(daily_demand['gas_usage_kWh']))
baseload_electricity = round(min(daily_demand['electricity_usage_kWh']))
peak_heating = round(max(hourly_demand['gas_usage_kWh']))
peak_electricity = round(max(hourly_demand['electricity_usage_kWh']))


# Calculate average thermal hourly demand, and size geothermal system.
average_heating = annual_heating/8760
geothermal_system = geothermal_system.geothermal_system(average_heating)
hourly_demand['geothermal_kWh'] = geothermal_system

# Pull in solar data
solar = solar.get_solar(start_date, end_date, lat, long, solar_area, panel_efficiency)
hourly_demand['solar_kWh'] = solar['solar_production_kWh']

# Calculate mismatch
hourly_demand['thermal_mismatch'] = hourly_demand['gas_usage_kWh'] - hourly_demand['geothermal_kWh']
thermal_deficit = round(sum(i for i in hourly_demand['thermal_mismatch'] if i > 0))
thermal_surplus = round(sum(i for i in hourly_demand['thermal_mismatch'] if i < 0))


#Printing statistics
print(f"Annual thermal demand is {annual_heating} kWh")
print(f"Annual electricity demand is {annual_electricity} kWh")
print(f"Baseload (24h) thermal demand is {baseload_heating} kWh")
print(f"Baseload (24h) electricity demand is {baseload_electricity} kWh")
print(f"Peak thermal demand is {peak_heating} kW")
print(f"Peak electricity demand is {peak_electricity} kW")
print(f"The total excess geothermal energy produced in the summer is {thermal_surplus} kWh and the "
      f"total geothermal energy deficit in the winter is {thermal_deficit} kWh.")
# Plotting
# demand.plot(y = ['gas_usage_kWh','geothermal_kWh'])
# plt.show()