from datetime import datetime
import time
import os
import numpy as np
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from math import sin, asin, cos, radians, fabs, sqrt,degrees
import pymongo

EARTH_RADIUS=6371
distance = 5

# 配置数据库信息
mongo_host = 'localhost'
mongo_db = 'python_test' # 数据库名
mongo_tb = 'python_test' # 表名

# 连接数据库
client = pymongo.MongoClient(mongo_host)
db = client[mongo_db]

def tick():
    print('Tick! The time is: %s' % datetime.now())
    try:
        if db[mongo_tb].find():
            print('mongo查询到有此条数据')
            db[mongo_tb].remove({})
            print('已删除')

    except Exception:
        print('删除MongoDb中数据失败')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # 间隔10秒钟执行一次
    scheduler.add_job(tick, 'interval', seconds=8)
    # 这里的调度任务是独立的一个线程
    scheduler.start()

    try:
        # 其他任务是独立的线程执行
        while True:
            df = pd.read_csv('D:/coordinate/log/2019042810.txt', encoding='utf-8')
            for i in range(len(df)):
                power = df.loc[i][1]
                tel = {'tel': df.loc[i][0]}
                time.sleep(2)
                try:
                    if list(db[mongo_tb].find(tel)):
                        print('有此条数据', tel)
                        continue

                    else:
                        print('之前没有此条数据', tel)
                        db[mongo_tb].insert(tel)
                except Exception:
                    print('存储到MongoDb失败')

                # if power == 30 or power == 25:
                dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(df.loc[i][2]))
                # 计算坐标点周围5km，南北两侧距离坐标
                dlat = distance / EARTH_RADIUS
                dlat = degrees(dlat)  # 弧度转换成角度
                dlng = degrees(dlng)  # 弧度转换成角度
                # cor1左上角坐标点，cor2右下角坐标点
                lat1, lng1 = df.loc[i][3] + dlat, df.loc[i][2] - dlng
                lat2, lng2 = df.loc[i][3] - dlat, df.loc[i][2] + dlng
                print('左右坐标点', lat1, lat2)
                time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print('Exit The Job!')




