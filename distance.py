#计算车辆方圆5km的坐标点
import os
import numpy as np
import pandas as pd
from math import sin, asin, cos, radians, fabs, sqrt,degrees

"""
def areas(distance,lat_lng):
    #计算坐标点周围5km，东西两侧距离,lat表示纬度，lng表示经度
    dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(lat_lng[0]))
    dlng = degrees(dlng)        # 弧度转换成角度
    
    #计算坐标点周围5km，南北两侧距离
    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)     # 弧度转换成角度

    lat1,lng1 = (lat_lng[0] + dlat,lat_lng[1] - dlng)
    lat2,lng2 = (lat_lng[0] - dlat,lat_lng[1] + dlng)

    print('left-top : ',(lat1, lng1))
    print('right-bottom:', (lat2, lng2))
    
# distance = input('请输入查找的范围半径：')
distance = 5

# lat_lng = pd.rea

lat_lng = (121.38538320556641,31.111198492236944)
EARTH_RADIUS=6371 #地球半径
areas(distance,lat_lng)

"""

#两坐标间距离
from math import radians,cos, sin, asin, sqrt, fabs
EARTH_RADIUS=6371           # 地球平均半径，6371km
 
def hav(theta):
    s = sin(theta / 2)
    return s * s
 
def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
 
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
 
    return distance
 
lon1,lat1 = ( 31.111198492236944,121.38538320556641) #上海莘庄地铁站
lon2,lat2 = ( 31.13059663612296,121.40276391998292) #上海莲花路地铁站 (高德地图驾车：2.8km)
d2 = get_distance_hav(lon1,lat1,lon2,lat2)
print(d2)  #得到的距离/km



