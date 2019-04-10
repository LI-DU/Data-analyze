#!/usr/bin/env python
#--*-- coding:utf-8 --*--

#python根据一个给定经纬度的点，进行附近5km距离坐标查询
import pymysql
import os
import subprocess
import time
import numpy as np
import pandas as pd
from math import sin, asin, cos, radians, fabs, sqrt,degrees

#读取车辆坐标位置文件
def get_cortxt():
    df = pd.read_csv('D:/cor.txt',encoding='utf-8',header=None,sep=' ')
    for i in range(len(df)):
        coordinate = df.loc[i]
        cor_areas(coordinate)
        
#计算坐标点周围5km，东西两侧距离,lat表示纬度，lng表示经度
def cor_areas(coordinate):
    dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(coordinate[1]))
    dlng = degrees(dlng)        # 弧度转换成角度

    #计算坐标点周围5km，南北两侧距离坐标
    dlat = distance / EARTH_RADIUS
    dlat = degrees(dlat)     # 弧度转换成角度
    
    #cor1左上角坐标点，cor2右下角坐标点
    cor1_vin,cor1_lat,cor1_lng = coordinate[0],coordinate[1] + dlat,coordinate[2] - dlng
    cor2_vin,cor2_lat,cor2_lng = coordinate[0],coordinate[1] - dlat,coordinate[2] + dlng

    mysql_query(cor1_lat,cor1_lng,cor2_lat,cor2_lng)
    #     mysql_query(32.006447,118.003882,31.096447,118.903882)


#将车辆坐标传入mysql数据库查询附近充电站的位置信息
def mysql_query(cor1_lat,cor1_lng,cor2_lat,cor2_lng):
        # sql中查询在此坐标5km范围内的充电站坐标
        import pymysql
        db = pymysql.connect(host='106.15.223.235', port=3306, user='readonly', password='abc123$%',
                             database='renwochong', charset='utf8')
        cursor = db.cursor()
#         select_cord = """select addr from t_charging_station where latitude > cor2_lat and latitude < cor1_lat and longitude > cor1_lng and longitude < cor2_lng"""
        select_cord = """select addr from t_charging_station where latitude > %f and latitude < %f and longitude > %f and longitude < %f"""%(cor2_lat,cor1_lat,cor1_lng,cor2_lng)
        #执行相关查询
        try:
            res = cursor.execute(select_cord)
            res = cursor.fetchall()
            print(res)
        except Exception as e:
            print(e)

#主函数部分
if __name__ == '__main__':
    EARTH_RADIUS=6371 #地球半径
    distance = 5  #车辆周围距离5km
    get_cortxt()


