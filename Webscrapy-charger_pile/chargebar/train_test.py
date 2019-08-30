import requests
import numpy
import urllib
import time
import re
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver
from geopy.geocoders import baidu
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
# 百度地图API搜索
def baidu_search(query, region,pageno):
    url = 'http://api.map.baidu.com/place/v2/search?'
    output = 'json'
    ak = '7d9u5nF8tlfpUcRCh5GFkW1P9gkOrp9T'
    uri = url + 'query=' + query + '&region=' + region  + '&page_size=' + '&page_num=' + str(pageno) + '&output=' + output + '&ak=' + ak

    r = requests.get(uri)
    response_dict = r.json()
    results = response_dict["results"]
    print(region,len(results))
'''

'''
    for adr in results:
        name = adr['name']
        # location = adr['location']
        address = adr['address']
        # telephone = adr['telephone']
        # lng = float(location['lng'])
        # lat = float(location['lat'])
        print('名称：' + name)
        print('地址：' + address)
        # print('电话：' + telephone)
        # print('坐标：%f,%f' % (lat, lng))
'''
company_name = '特来电'
top = ['北京市','上海市','深圳市','广州市']
city_name = ['成都市','杭州市','重庆市','武汉市','苏州市','西安市','天津市','南京市','郑州市','长沙市','沈阳市','青岛市','宁波市',
        '东莞市','无锡市','昆明市','大连市','厦门市','合肥市','佛山市','福州市','哈尔滨市','济南市','温州市','长春市','石家庄市','常州市','泉州市','南宁市',
        '贵阳市','南昌市','南通市','金华市','徐州市','太原市','嘉兴市','烟台市','惠州市','保定市','台州市','中山市','绍兴市','乌鲁木齐市','潍坊市','兰州市',
        '珠海市','镇江市','海口市','扬州市','临沂市','洛阳市','唐山市','呼和浩特市','盐城市','汕头市','廊坊市','泰州市','济宁市','湖州市','江门市','银川市',
        '淄博市','邯郸市','芜湖市','漳州市','绵阳市','桂林市','三亚市','遵义市','咸阳市','上饶市','莆田市','宜昌市','赣州市','淮安市','揭阳市','沧州市','商丘市',
        '连云港市','柳州市','岳阳市','信阳市','株洲市','衡阳市','襄阳市','南阳市','威海市','湛江市','包头市','鞍山市','九江市','大庆市','许昌市','新乡市','宁德市',
        '西宁市','宿迁市','菏泽市','蚌埠市','邢台市','铜陵市','阜阳市','荆州市','驻马店市','湘潭市','滁州市','肇庆市','德阳市','曲靖市','秦皇岛市','潮州市','吉林市','常德市','宜春市','黄冈市']
for city in top:
    for i in range(0,20):

        url = 'http://api.map.baidu.com/place/v2/search?'
        output = 'json'
        ak = '7d9u5nF8tlfpUcRCh5GFkW1P9gkOrp9T'
        uri = url + 'query=' + company_name + '&region=' + city + '&page_size=' + '&page_num=' + str(i) + '&output=' + output + '&ak=' + ak

        r = requests.get(uri)
        response_dict = r.json()
        results = response_dict["results"]
        print(city, len(results))

