from bs4 import BeautifulSoup as soup
import requests


req = requests.get("https://wildfiretoday.com/recent-fires/page/2/")

sp = soup(req.content,'html5lib')

data_name = sp.find_all('div',attrs={'class':"entry-content"})
result=[]
if data_name != 0:
    for d in data_name:
        list=d.find_all('p')
        temp = ""
        for ld in list:
            temp+=ld.getText()
        result.append(temp)
