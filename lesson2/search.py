# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 23:18:37 2019

@author: lenovo
"""
import requests
import re

from bs4 import BeautifulSoup
url = 'https://www.bjsubway.com/station/xltcx/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
response = requests.get(url, headers = headers, allow_redirects=False,verify=False)
response.encoding="gb2312"
soup = BeautifulSoup(response.content, 'lxml')

table = soup.findAll('div', attrs={'class':"line_content"})
#print((table))
nameList = []
stationDic= {}

for i in table:
    rows = i.findAll('div',attrs={'class':"line_name"})
    for row in rows:
            cols = row.find('div')
            if cols != None:
               name = cols.text.strip()
               nameList.append(name)
           
print(nameList)
print(stationDic)
curName = ''
for i in table:
    rows = i.findAll('div')
    for row in rows:
        if row['class']== ['line_name']:
              curName = row.find('div').text.strip()
              stationDic[curName] = []
        else :
            if row['class']== ['station']:
                 station = row.text.strip()
                 stationDic[curName].append(station)
print(stationDic)                
           

