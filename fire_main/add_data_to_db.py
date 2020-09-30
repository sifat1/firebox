import numpy as np
import pandas as pd
import reverse_geocode as rg
#from fire_main.models import fire_info
#from fire_main.models import fire_info


#fire_inf = fire_info()
# read data from csv
DF = pd.read_csv(u"./data/modis_1km/MODIS_C6_USA_contiguous_and_Hawaii_48h.csv")

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
    #fire_inf.latitude = lat[i][0]
    #fire_inf.longitude = lan[i][0]
    coordinates = [(float(lat[i][0]),float(lan[i][0]))]

    #print(coordinates)
    result=rg.search(coordinates)
    ##fire_inf.city = result[0]['city']
    #fire_inf.country = result[0]['country']
    #fire_inf.brightness_temp = kelvin_to_degree(reflectance[i][0])
    #print(city.lower(),country.lower(),reflectance_temp)
    #fire_inf.frp = frp[i]
    #fire_inf.date = date[i]
    print(result[0])
    #print(result[0]['city']," ",result[0]['country'])
    break
