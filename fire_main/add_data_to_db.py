import numpy as np
import pandas as pd
import reverse_geocode as rg
# read data from csv

DF = pd.read_csv("./data/modis_1km/MODIS_C6_USA_contiguous_and_Hawaii_48h.csv")

Filtered = DF[DF.confidence>=100]

lat = np.array(Filtered[['latitude']])
lan = np.array(Filtered[['longitude']])
reflectance = np.array(Filtered[['brightness']])
frp = np.array(Filtered[['frp']])
date = np.array(Filtered[['acq_date']])

full_len = len(lat)

def kelvin_to_degree(kelvin_value):
    return kelvin_value + 273.0
for i in range(full_len):
    coordinates = [(lat[i][0],lan[i][0])]
    result=rg.search(coordinates)
    city = result[0]['city']
    country = result[0]['country']
    reflectance_temp = kelvin_to_degree(reflectance[i][0])
    print(city,country,reflectance_temp)
