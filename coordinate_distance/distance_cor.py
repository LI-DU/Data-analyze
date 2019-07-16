#!/usr/bin/env python
#--*-- coding:utf-8 --*--

"""从车辆坐标日志文件中实时读取日志内容，根据车辆经纬度，从充电运营平台数据库
查询周围5km公司运营的充电站，如果能查到，将站点名称返回"""

import os
import time
import codecs
import sys
import types
import pymysql
import json
import subprocess
import numpy as np
import pandas as pd
from flask import render_template
from flask import Flask,jsonify

from datetime import datetime
from math import sin, asin, cos, radians, fabs, sqrt,degrees

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

EARTH_RADIUS=6371   #地球半径
time_day = datetime.now().strftime('%Y%m%d')   #今天日期 

#获取当天最新生成的日志文件
def get_the_new_file():
    files = os.listdir(path)
    files_list = list(filter(lambda x:x[-4:]=='.log' and x[0:8]==time_day, files))    #列出当前目录下今天的日志文件
    files_list.sort(key=lambda fn:os.path.getmtime(path + '/' + fn) if not os.path.isdir(path + '/' + fn) else 0)
    new_file = os.path.join(path, files_list[-1])    #汇总今天生成的日志，并取最新生成的日志返回
    return new_file

#获取日志文件大小
def get_file_size(new_file):
    fsize = os.path.getsize(new_file)
    fsize = fsize/float(1024*1024)    #计算日志文件大小，以M为单位
    return fsize

#读取当天最新的日志文件，系统默认20M分割一个日志文件，
# 如果文件大小大于20M，则自动结束读取当前文件，转到读取下个生成的文件
def tail_cor_log():
    while True:
        new_file = get_the_new_file()
        p = subprocess.Popen('tail -f {0}'.format(new_file), shell=True, 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,)    #起一个进程，执行tail日志的shell命令
        while True:
            line = p.stdout.readline()   #实时获取行
            if line:                     #如果行存在，执行下面
                if get_file_size(new_file) > 20:    #如果大于20M，则跳出循环
                    break

                split_line = line.decode().split()    #获取到的line数据类型为bytes，先decode解码为str，然后split以空格分组
                pd_line = pd.DataFrame(split_line)    #将数据类型转为Dataframe
                
                vin = str(pd_line.loc[1])
                lat = float(pd_line.loc[1])           #取坐标数据的纬度
                lng = float(pd_line.loc[2])
                coordinate = (vin,lat,lng)


                # 计算坐标点周围5km，东西两侧距离,lat表示纬度，lng表示经度
                dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(coordinate[1]))
                dlng = degrees(dlng)  # 弧度转换成角度

                # 计算坐标点周围5km，南北两侧距离坐标
                dlat = distance / EARTH_RADIUS
                dlat = degrees(dlat)  # 弧度转换成角度

                # cor1左上角坐标点，cor2右下角坐标点
                cor1_lat, cor1_lng = coordinate[1] + dlat, coordinate[2] - dlng
                cor2_lat, cor2_lng = coordinate[1] - dlat, coordinate[2] + dlng
                coor = cor1_lat, cor1_lng, cor2_lat, cor2_lng
                return coor


#将车辆坐标传入mysql数据库查询附近充电站的位置信息
@app.route('/coordinate',methods=['POST','GET'])
def mysql_query():

    coor_t = tail_cor_log()
    cor1_lat, cor1_lng, cor2_lat, cor2_lng = coor_t
    # sql中查询在此坐标5km范围内的充电站坐标
    db = pymysql.connect(host='106.15.223.235', port=3306, user='readonly', password='abc123$%',
                database='renwochong', charset='utf8')
    cursor = db.cursor()

    select_cord = """select cast(longitude AS CHAR ),cast(latitude AS CHAR ) from t_charging_station where latitude > %f and latitude < %f and longitude > %f and longitude < %f"""%(cor2_lat,cor1_lat,cor1_lng,cor2_lng)
    #执行相关查询
    try:
        res_exc = cursor.execute(select_cord)
        res = cursor.fetchall()
        list_res = list(res)
        list01 = []
        for i in range(len(list_res)):
            coor = {'lng': float(list_res[i][0]), 'lat': float(list_res[i][1])}
            list01.append(coor)
        dic = {'coordinate': list01}
        return jsonify(dic)

    except Exception as e:
        print(e)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#主函数部分
if __name__ == '__main__':
    path = '/home/admin/LOG'
    distance = 5  #车辆周围距离5km
    app.run(
        host='localhost',
        port=8000,
        debug=True)
    