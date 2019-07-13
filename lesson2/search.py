# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 23:18:37 2019

@author: lenovo
"""
import json
import requests
import re
import math
from bs4 import BeautifulSoup
#通过北京地铁百科获取北京地铁的详细信息
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
url = 'https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485'
response = requests.get(url, headers = headers, allow_redirects=False)
response.encoding="utf-8"
soup = BeautifulSoup(response.content, 'lxml')
table = soup.findAll('table', attrs={'log-set-param':"table_view",'data-sort':"sortDisabled"})
lineDic= {}
for i in table:
    rows = i.findAll('tr')
    for row in rows:
            cols = row.findAll('td')
            if len(cols) > 0:
                href = cols[0].find_all('a',{'href':re.compile("\/item.*"),'data-lemmaid' : ''})
                for item in href:                
                       website = item.get('href') 
                       name = item.text.strip()
                       lineDic[name]= website
                      
#print(lineDic)
#url = 'https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%8115%E5%8F%B7%E7%BA%BF'
url = 'https://baike.baidu.com' + lineDic['北京地铁15号线']
response = requests.get(url, headers = headers, allow_redirects=False)
response.encoding="utf-8"
soup = BeautifulSoup(response.text, 'lxml')
#15号线
table15 = soup.findAll('table', attrs={'class':"fifteen",'log-set-param':"table_view" ,'data-sort':"sortDisabled", 'width':"658"})
#print(len(table15))
stationName = []
for i in table15:
        rows = i.findAll('tr')
        for row in rows:
            cols = row.findAll('th')# 15号线
            if cols != None  and cols != []:
                 #print(cols)
                 s = cols[0].text.strip()
                 p = re.match( r'(.*)——.*', s)
                 #print(p)
                 if p != None or s == '车站名称' or s == '起始/终到车站':
                     continue
                 else:
                     stationName.append(s)
       
#获得了15号线的所有站点  
print('15号线的所有站点') 
print(stationName)
#因为北京地铁百科数据读取比较复杂，后来改为读取北京地铁官网的数据了
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
           
#print(nameList)
#print(stationDic)
#获取北京地铁所有线路对应的站点信息
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
#print(stationDic)  
def writefileContentTOFile(_content):
    with open("station.txt", 'w'
              ,encoding='utf-8') as f:#文件名不能当作参数传
         for a in _content:
             f.write(str(a) + '\n') 
#北京地铁14号线的数据每个站点的顺序不对，所以这块我重新赋值了            
stationDic['14号线'] = [ "善各庄","来广营", "东湖渠", "望京","阜通",  "望京南","将台","东风北桥", "枣营", "朝阳公园","金台路","大望路",   "九龙山", "平乐园" ,"北工大西门", "十里河","方庄", "蒲黄榆", "景泰", "永定门外","北京南站"]            
           
#with open('station.json','w',encoding='utf-8') as f:
 # json.dump(stationDic,f,ensure_ascii=False)
# 从文件读取数据
#读的时候总是报错 还没解决这个问题，如果老师有时间了希望帮我看一下
'''
with open('station2.json','r',encoding='UTF-8') as f:
   stationDic = json.load(f)
   if stationDic.startswith(u'\ufeff'):
     #stationDic = stationDic.encode('utf-8')[3:].decode('utf-8')
'''
connection_info_src = {}           
for k,v in enumerate(stationDic):
    for idx, val in enumerate(stationDic[v]):
         if val not in connection_info_src.keys():
              connection_info_src[val] = []
         if idx > 1:
              connection_info_src[val].append(stationDic[v][idx -1])
         if idx + 1 < len(stationDic[v]):
              connection_info_src[val].append(stationDic[v][idx+1])
#print(connection_info_src)
#2号线 10号线是环路，所以进行了手动处理              
connection_info_src['西直门'].append('车公庄')
connection_info_src['车公庄'].append('西直门')
connection_info_src['巴沟'].append('火器营')
connection_info_src['火器营'].append('巴沟')
#print(connection_info_src)

#如果两个站是同一个地铁线，返回该地铁线
def chechIsSameLine(start,end):
    for k,v in enumerate(stationDic):
       if stationDic[v].count(start) == 1 and stationDic[v].count(end) == 1:
            return v
    return None

def search(start, destination, connection_grpah, sort_candidate):
    pathes = [[start]]
    visitied = set()
    
    while pathes: # if we find existing pathes
        path = pathes.pop(0)
        froninter = path[-1]
        if froninter in visitied: continue
        successors = connection_grpah[froninter]
        for city in successors:
            if city in path: continue  # eliminate loop
                
            new_path = path + [city]
            
            pathes.append(new_path)
            
            if city == destination:
               return new_path
        visitied.add(froninter)
        pathes = sort_candidate(pathes) # 我们可以加一个排序函数 对我们的搜索策略进行控制
def transfer_stations_less(pathes): 
    return sorted(pathes, key=len)
def transfer_stations_first(pathes): 
    return sorted(pathes, key=len)
def transfer_as_much_possible(pathes):
    return sorted(pathes, key=len, reverse=True)
#按照换乘最少排序
def transfer_station_less_2(pathes):
    if len(pathes) <= 1: return pathes
    
    def get_transfter(path):
        line = []
        for k,v  in enumerate(path[0:-2]):
            #print(v + "+" + path[k+1])
            temp = chechIsSameLine(v, path[k+1])
            if line.count(temp):
                continue
            else:
                line.append(temp)
            
        return len(line)
    return sorted(pathes, key=get_transfter)
def shortest_path_first(pathes):
    
    if len(pathes) <= 1: return pathes
    
    def get_path_distnace(path):
        distance = 0
        for station in path[:-1]:
            distance += get_geo_distance(station, path[-1])
            
        return distance

    return sorted(pathes, key=get_path_distnace)
def get_geo_distance(origin, destination):
    
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d
#按照最少换乘排序
s = search('劲松','霍营',connection_info_src, sort_candidate=transfer_station_less_2)
print('=>'.join(s))
