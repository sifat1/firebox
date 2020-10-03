from django.shortcuts import render,redirect
from django.http import HttpResponse
from fire_main.models import fire_info,set_user_location,fire_economic_data
from django.contrib.auth.models import User,auth
from django.http import JsonResponse
import reverse_geocode as rg
import geopy.distance
from datetime import date
import requests

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import os
import math
import cv2
import numpy as np
# Create your views here.

def index(request):
    print(request.path)
    #save_info()
    return render(request,'fire_main/index.html')
def veg_data(request):
    if 'lat' in request.POST:
        lat = request.POST['lat']
        lon = request.POST['lon']
        val_ = str(get_mx(lat,lon))
        return render(request,'fire_main/locationpicker_vg.html',{'val_': val_})
    return render(request,'fire_main/locationpicker_vg.html')

def pick_location(request):
    return render(request,'fire_main/location_picker.html')

def login_signup(request):
    return render(request,'fire_main/login.html')
def signup(request):
    if request.method == "GET":
        return render(request,'fire_main/login.html')
    else:
        try:
            user = User.objects.create_user(username=request.POST['user_name'],password=request.POST['password']
            ,email=request.POST['email'])
            user.save()

            #print(request.FILES['profile_img'])
        except Exception as e:
            print(e)
            response_="This User already exist!"
            return render(request,'fire_main/login.html',{'response':response_})
        return redirect('/')
def set_user_location(request):
    lat = request.POST['lat']
    lon = request.POST['lon']
    coordinates = [(lat,lon)]
    result=rg.search(coordinates)
    user_loc = set_user_location()
    user_loc.lat = lat
    user_loc.lon = lon
    user_loc.city = result[0]['city']
    user_loc.country = result[0]['country']
    user_loc.date =  date.today()

def get_user_loaction(request):
    fire_ec = fire_economic_data.objects.all()
    damage = ""
    area = ""
    city = ""
    country = ""
    city_country_list = []
    count = 0
    for r in fire_ec:
        damage = r.details
        area = float(r.area_expected)
        city = r.city
        country = r.country
        city_country_list.append(r.city+","+r.country)
        count = fire_info.objects.filter(city=city,country=country).count() + 1
        area = round(area * count,2)
        #print("Burning : "+str(count+1)+"km")

    if 'lat' in request.POST:
        lat = request.POST['lat']
        lon = request.POST['lon']

        url_ = "http://api.airpollutionapi.com/1.0/aqi?lat="+lat+"&lon="+lon+"&APPID=oki0j2l7pq9h5p5pnvfh613ml7"
        r = requests.get(url = url_)
        data = r.json()
        co_index_bad = False

        if float(data['data']["aqiParams"][4]['aqi'])>200:
            co_index_bad = True

        co_index_data=data['data']["alert"]

        #co_index_data = "dummy"
        coordinates = [(lat,lon)]
        coords_1 = (lat,lon)
        #print(coordinates)
        result=rg.search(coordinates)
        low = True
        user_city = result[0]['city']
        user_country = result[0]['country']
        fire_inf = fire_info.objects.filter(city=user_city,country=user_country)
        distance=[]
        if len(fire_inf)!=0:
            for d in fire_inf:
                coords_2 = (d.latitude, d.longitude)
                distance.append(round(geopy.distance.geodesic(coords_1, coords_2).km,2))
            if max(distance) < 10 or co_index_bad==True:
                low = False
            else:
                low = True
        if low == True:
            #return render(request,"fire_main/index.html",{'response':'LOW'})
            return render(request,"fire_main/index.html",{'response':'LOW','damage': damage,'area': area,'city': city,'country': country,'city_country_list': city_country_list,'count': count,'co_index_data': co_index_data})
        else:
            return render(request,"fire_main/index.html",{'response':'High','damage': damage,'area': area,'city': city,'country': country,'city_country_list': city_country_list,'count': count,'co_index_data': co_index_data})
    elif 'location' in request.POST:
        data=request.POST['location'].split(",")
        count = fire_info.objects.filter(city=data[0],country=data[1]).count() + 1
        fire = fire_economic_data.objects.filter(city=data[0],country=data[1])
        city = data[0]
        country = data[0]
        print(count)
        for f in fire:
            damage = f.details
            area = float(f.area_expected)
            area = round(area * count,2)
        return render(request,"fire_main/index.html",{'response':'Undefined','damage': damage,'area': area,'city': city,'country': country,'city_country_list': city_country_list,'count': count})
    else:
        return render(request,"fire_main/index.html",{'damage': damage,'area': area,'city': city,'country': country})


def dl_file(minlat,minlon,maxlat,maxlon,date):
    options = Options()
    path_ = "C:\\Users\\ASUS\\Documents\\Space App\\download file\\"+"folder_"+str(minlat)+str(minlon)+str(maxlat)+str(maxlon)
    if os.path.exists(path_) == False:
        os.mkdir(path_)
    file_location = path_
    options.add_experimental_option("prefs",{"download.default_directory": path_})
    drive = webdriver.Chrome(executable_path=r"C://Users/ASUS/Documents/Space App/download file/chromedriver.exe",chrome_options=options)

    drive.get("https://wvs.earthdata.nasa.gov/?LAYERS=MODIS_Terra_CorrectedReflectance_Bands721&CRS=EPSG:4326&TIME=2020-09-26&COORDINATES="+str(minlat)+","+str(minlon)+","+str(maxlat)+","+str(maxlon)+"&FORMAT=image/png&AUTOSCALE=TRUE&RESOLUTION=250m")

    button = drive.find_element_by_id("button-download")

    button.click()
    time.sleep(20)
    wait = True
    while(wait==True):
        for fname in os.listdir(path_):
            if ('crdownload') in fname:
                print('downloading files ...')
                time.sleep(10)
            else:
                wait=False
                print('finished downloading all files ...')
    drive.close()

def get_img(minlat,minlon,maxlat,maxlon):
    date1 = "2020-09-26"
    date2 = "2020-09-24"
    dl_file(minlat,minlon,maxlat,maxlon,date1)
    dl_file(minlat,minlon,maxlat,maxlon,date2)
def get_image_vg(path_to_img):
    img = cv2.imread(path_to_img)  #Best practise is to specify the flag you want set, confirming you want a colour picture.

    # converting from BGR to HSV color space
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (40, 25, 25), (89, 255,255))

    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]
    bgrimg = cv2.cvtColor(green, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(bgrimg, cv2.COLOR_BGR2GRAY)/255
    nzCount = cv2.countNonZero(gray)

    return nzCount

def get_mx(lat, lng, radiusInKm=1):
  lat_change = radiusInKm/111.2
  lon_change = math.fabs(math.cos(lat*(math.pi/180)))
  min_lat=lat - lat_change-1
  min_lng=lng - lon_change
  max_lat=lat + lat_change+1
  max_lng=lng + lon_change
  get_img(min_lat,min_lng,max_lat,max_lng)

  path_ = "C:\\Users\\ASUS\\Documents\\Space App\\download file\\"+"folder_"+str(min_lat)+str(min_lng)+str(max_lat)+str(max_lng)
  arr = os.listdir(path_)


  now = get_image_vg(path_+"\\"+arr[0])
  previous = get_image_vg(path_+"\\"+arr[1])

  return (previous - now)/now
