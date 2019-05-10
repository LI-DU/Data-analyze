import time
import pymysql
import numpy as np
import pandas as pd
from datetime import datetime
from lib.yuntongxun.sms import CCP
from flask import Flask,jsonify,request
from pymongo import MongoClient,InsertOne
from math import sin, asin, cos, radians, fabs, sqrt,degrees

EARTH_RADIUS=6371
distance = 5
app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/',methods=['POST','GET'])
def mysql_query():
    #连接monogodb
    conn_mongo = MongoClient('127.0.0.1:27017',maxPoolSize=None)
    db_mon = conn_mongo.python_test #database
    db_collection = db_mon.test_01 #table

    df = pd.read_csv('D:/coordinate/log/2019042810.txt', encoding='utf-8')
    for i in range(len(df)):
        power = df.loc[i][1]
        tel = df.loc[i][0]
        print(power)
        if power == 30 or power == 20:
            dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(df.loc[i][2]))
            # 计算坐标点周围5km，南北两侧距离坐标
            dlat = distance / EARTH_RADIUS
            dlat = degrees(dlat)  # 弧度转换成角度
            dlng = degrees(dlng)  # 弧度转换成角度
            # cor1左上角坐标点，cor2右下角坐标点
            lat1, lng1 = df.loc[i][3] + dlat, df.loc[i][2] - dlng
            lat2, lng2 = df.loc[i][3] - dlat, df.loc[i][2] + dlng
            print(lat1, lat2)
            # if lat1:
            #     CCP().send_template_sms(13002106696, [12345, 5], 1)

            # sql中查询在此坐标5km范围内的充电站坐标
            db = pymysql.connect(host='106.15.223.235', port=3306, user='readonly', password='abc123$%',
                                 database='renwochong', charset='utf8')
            cursor = db.cursor()

            select_cord = """select cast(longitude AS CHAR ),cast(latitude AS CHAR ) from t_charging_station where latitude > %s and latitude < %s and longitude > %s and longitude < %s""" % (
            lat2, lat1, lng1, lng2)  # (lat_lng[2],lat_lng[0],lat_lng[1],lat_lng[3])

            # select_cord = """select longitude,latitude from t_charging_station where latitude > 30.0105 and latitude < 31.8519 and longitude > 118.3307 and longitude < 120.1725"""
            # 执行相关查询

            try:
                res_exc = cursor.execute(select_cord)
                res = cursor.fetchall()
                if res:
                    list_res = list(res)
                    list01 = []
                    for i in range(len(list_res)):
                        coor = {'lng': float(list_res[i][0]), 'lat': float(list_res[i][1])}
                        list01.append(coor)
                    dic = {'coordinate': list01}
                    print(dic)
                    # if dic:
                    #     CCP().send_template_sms(13002106696, [66666, 5], 1)
                    return jsonify(dic)

            except Exception as e:
                print(e)

        else:
            return '000'


'''
@app.route('/',methods=['POST','GET'])
def test_json():
    list01 = []
    list_res = [('119.0623670', '31.6680730'), ('119.0396010', '31.6368940'), ('119.0350660', '31.6573290')]
    for i in range(len(list_res)):
        coor = {'lng': float(list_res[i][0]), 'lat': float(list_res[i][1])}
        list01.append(coor)
    dic = {'coordinate':list01}
    return jsonify(dic)
    # return json.dumps(t, ensure_ascii=False)  #也可以用json.dumps返回json数据
'''

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,session_id')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    # 这里不能使用add方法，否则会出现 The 'Access-Control-Allow-Origin' header contains multiple values 的问题
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

#主函数部分
if __name__ == '__main__':
    app.run(
        host='localhost',
        port=8000,
        debug=True,
        threaded=True)