from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import numpy as np
import pandas as pd
import reverse_geocode as rg
import requests
import pickle
from sklearn.ensemble import RandomForestRegressor
#from fire_main.models import fire_info
from fire_main.models import fire_info, fire_economic_data
logger = get_task_logger(__name__)
def add_csv_data_to_db():

    # read data from csv
    DF = pd.read_csv("./fire_main/data/modis_1km/MODIS_C6_USA_contiguous_and_Hawaii_48h.csv")

    Filtered = DF[DF.confidence>=100]

    lat = np.array(Filtered[['latitude']])
    lan = np.array(Filtered[['longitude']])
    reflectance = np.array(Filtered[['brightness']])
    frp = np.array(Filtered[['frp']])
    date = np.array(Filtered[['acq_date']])

    full_len = len(lat)

    def kelvin_to_degree(kelvin_value):
        return kelvin_value - 273.15

    for i in range(full_len):
        fire_inf = fire_info()
        fire_inf.latitude = lat[i][0]
        fire_inf.longitude = lan[i][0]

        coordinates = [(float(lat[i][0]),float(lan[i][0]))]

        #print(coordinates)
        result=rg.search(coordinates)

        fire_inf.city = result[0]['city']
        fire_inf.country = result[0]['country']
        fire_inf.brightness_temp = kelvin_to_degree(reflectance[i][0])
        #print(city.lower(),country.lower(),reflectance_temp)
        fire_inf.frp = frp[i][0]
        fire_inf.date = date[i][0]
        fire_inf.save()
        print(result[0]['city'])

def add_area_prediction():
    fire_inf = fire_info.objects.all()
    data1=set()
    for d in fire_inf:
        data1.add(d.city+","+d.country)
    for d in data1:
        fire = fire_economic_data()
        data = d.split(",")
        print(data[0],data[1])
        r = requests.get(url = "http://api.openweathermap.org/data/2.5/weather?q="+data[0]+"&appid=d7bd9aba0a110bf6c6f417e67c290b68")
        w_data = r.json()
        temp = w_data['main']['temp'] - 273.15
        rhm = w_data['main']['humidity']
        wind  = w_data['wind']['speed']
        loaded_model = pickle.load(open("model.sav", 'rb'))
        result = loaded_model.predict(np.array([[temp,rhm,wind]]))
        print(result)
        fire.city = data[0]
        fire.country = data[1]
        fire.details = ""
        fire.area_expected = str(result)
        fire.save()

def add_data_with_wcr():
    pass


@periodic_task(run_every=(crontab(minute='*/15')),name="update_db",ignore_result=True)
def update_db():
    logger.info("db started")
    #add_csv_data_to_db()
    add_area_prediction()
