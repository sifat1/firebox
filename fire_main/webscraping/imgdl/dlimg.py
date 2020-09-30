from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import os

def get_img(minlat,minlon,maxlat,maxlon):
    options = Options()
    path = "C://Users/ASUS/Documents/Space App/download file/"+"_"+str(minlat)+str(minlon)+str(maxlat)+str(maxlon)
    os.mkdir(path)
    file_location = path
    options.add_experimental_option("prefs",{"download.default_directory": file_location})
    drive = webdriver.Chrome(executable_path=r"C:\Users\ASUS\Documents\Space App\download file\chromedriver.exe",chrome_options=options)

    drive.get("https://wvs.earthdata.nasa.gov/?LAYERS=MODIS_Terra_CorrectedReflectance_Bands721&CRS=EPSG:4326&TIME=2020-09-23&COORDINATES="+str(minlat)+","+str(minlon)+","+str(maxlat)+","+str(maxlon)+"&FORMAT=image/png&AUTOSCALE=TRUE&RESOLUTION=250m")

    button = drive.find_element_by_id("button-download")

    button.click()
    time.sleep(20)
    wait = True
    while(wait==True):
        for fname in os.listdir(r"C:\Users\ASUS\Documents\Space App\download file\newtemp1"):
            if ('crdownload') in fname:
                print('downloading files ...')
                time.sleep(10)
            else:
                wait=False
                print('finished downloading all files ...')
    #drive.close()

get_img(11.395569,36.650391,12.691956,38.210449)
