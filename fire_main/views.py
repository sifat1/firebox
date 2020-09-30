from django.shortcuts import render,redirect
from django.http import HttpResponse
from fire_main.models import fire_info
from django.http import JsonResponse
import reverse_geocode as rg
import geopy.distance
# Create your views here.

def index(request):
    print(request.path)
    #save_info()
    return render(request,'fire_main/index.html')

def get_user_loaction(request):
    lat = request.POST['lat']
    lon = request.POST['lon']
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
            coords_2 = (52.406374, 16.9251681)
            distance.append(round(geopy.distance.geodesic(coords_1, coords_2).km,2))
        if distance.max() < 10:
            low = False
        else:
            low = True
    if low == True:
        #return render(request,"fire_main/index.html",{'response':'LOW'})
        return render(request,"fire_main/index.html",{'response':'LOW'})
