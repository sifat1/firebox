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

def send_sms(sms,number):
    url = "http://66.45.237.70/api.php?username=XX&password=XXX&number="+number+"&message="+sms
    payload  = {}

    headers = {

        'Content-Type': 'application/x-www-form-urlencoded'
        }
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
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

        #we will send sms here

def add_data_with_wcr():
    result=[]
    for pages in rage(12):
        req = requests.get("https://wildfiretoday.com/recent-fires/page/"+pages+"/")

        sp = soup(req.content,'html5lib')

        data_name = sp.find_all('div',attrs={'class':"entry-content"})
        if data_name != 0:
            for d in data_name:
                list=d.find_all('p')
                temp = ""
                for ld in list:
                temp+=ld.getText()
                result.append(temp)
    fire_inf = fire_info.objects.all()
    data1=set()
    for d in fire_inf:
        data1.add(d.city+","+d.country)
    for d in data1:
        data = d.split(",")
        for res in result:
            if data[0] in res:
                nlp = spacy.load("en_core_web_sm")
                matcher = Matcher(nlp.vocab)
                pattern = [{"POS": "VERB"},{"POS": "ADV","op": "?"}, {"POS": "NUM"}, {"POS": "NOUN"}]
                matcher.add("Damage", None, pattern)
                doc1 = nlp(res)
                matches = matcher(doc1)
                for match_id, start, end in matches:
                    string_id = nlp.vocab.strings[match_id]  # Get string representation
                    span = doc1[start:end]  # The matched span
                    if span.text!="":
                        obj = fire_info.objects.get(city=data[0])
                        obj.details = span.text
                        obj.save()


@periodic_task(run_every=(crontab(minute='*/15')),name="update_db",ignore_result=True)
def update_db():
    logger.info("db started")
    #add_csv_data_to_db()
    add_area_prediction()
