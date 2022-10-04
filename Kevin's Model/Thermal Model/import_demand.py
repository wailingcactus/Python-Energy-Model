import pandas as pd

def import_data(file):
    """This function requires a xlsx file name as an input, and returns the data in a pandas data frame"""
    demand = pd.read_excel('Delaware_Model_Data_2018.xlsx')
    #demand['monthyear']=pd.to_datetime(demand['datetime']).dt.strftime('%Y-%m')
    print(demand.to_string())
    return demand