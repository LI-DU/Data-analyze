import time
import pymysql
import threading
import schedule
import pymongo
import numpy as np
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from lib.yuntongxun.sms import CCP
from flask import Flask,jsonify,request
from apscheduler.schedulers.background import BackgroundScheduler
from math import sin, asin, cos, radians, fabs, sqrt,degrees

EARTH_RADIUS=6371
distance = 5
app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 配置数据库信息
mongo_host = 'localhost'
mongo_db = 'python_test'  # 数据库名
mongo_tb = 'python_test'  # 表名
# 连接数据库
mongoclient = pymongo.MongoClient(mongo_host)
mongodb = mongoclient[mongo_db]

def tick():
    print('Tick! The time is: %s' % datetime.now())
    try:
        if mongodb[mongo_tb].find():
            print('mongo查询到有此条数据')
            mongodb[mongo_tb].remove({})
            print('已删除')

    except Exception:
        print('删除MongoDb中数据失败')


def tail_log():
    try:
        # 其他任务是独立的线程执行
        # while True:
        df = pd.read_csv('D:/coordinate/log/2019042810.txt', encoding='utf-8')
        for i in range(len(df)):
            power = df.loc[i][1]
            tel = {'tel': df.loc[i][0]}
            print('号码是',tel)
            print(list(mongodb[mongo_tb].find(tel)))
            time.sleep(2)
            try:
                if list(mongodb[mongo_tb].find(tel)):
                    print('有此条数据', tel)
                    continue

                else:
                    print('之前没有此条数据', tel)
                    mongodb[mongo_tb].insert(tel)
            except Exception:
                print('存储到MongoDb失败')

        # df = pd.read_csv('D:/coordinate/log/2019042810.txt', encoding='utf-8')
        # for i in range(len(df)):
        #     power = df.loc[i][1]
        #     tel = {'tel':df.loc[i][0]}
            # if power == 30 or power == 25:
            dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(df.loc[i][2]))
            # 计算坐标点周围5km，南北两侧距离坐标
            dlat = distance / EARTH_RADIUS
            dlat = degrees(dlat)  # 弧度转换成角度
            dlng = degrees(dlng)  # 弧度转换成角度
            # cor1左上角坐标点，cor2右下角坐标点
            lat1, lng1 = df.loc[i][3] + dlat, df.loc[i][2] - dlng
            lat2, lng2 = df.loc[i][3] - dlat, df.loc[i][2] + dlng
            time.sleep(2)
            coordinate = (lat2, lat1, lng1, lng2, tel)
            return coordinate

    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')


@app.route('/', methods=['POST', 'GET'])
def mysql_query():
    coord = tail_log()
    lat2, lat1, lng1, lng2, tel = coord
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
        list_res = list(res)
        list01 = []
        for i in range(len(list_res)):
            coor = {'lng': float(list_res[i][0]), 'lat': float(list_res[i][1])}
            list01.append(coor)
        dic = {'coordinate': list01}

        # print('----dic0',dic)
        # mongo_tel = mongodb[mongo_tb].find(tel)
        # mongo_coor = mongodb[mongo_tb].find(tel),{'coor':dic}
        if list01:
            # if not mongo_coor:
            #     mongodb[mongo_tb].insert(tel)  #不要使用insertOne或者updateOne,不然会报错，是因为版本原因，没有insertOne方法，'Collection' object is not callable. If you meant to call the 'insert_one' method on a 'Collection' object it is failing because no such method exists.
            # CCP().send_template_sms(13002106696, [66666, 5], 1)
            #关闭游标和连接
            cursor.close()
            db.close()
            return jsonify(dic)
    except Exception as e:
        print(e)



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
    scheduler = BackgroundScheduler()
    # 间隔10秒钟执行一次
    scheduler.add_job(tick, 'interval', seconds=30)
    # 这里的调度任务是独立的一个线程
    scheduler.start()

    app.run(
        host='localhost',
        port=8000,
        debug=True,
        threaded=True)