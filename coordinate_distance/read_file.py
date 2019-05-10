import time
from apscheduler.schedulers.blocking import BlockingScheduler
from pymongo import MongoClient,InsertOne

def insert_tel():
    #连接数据库
    conn_mongo = MongoClient('127.0.0.1:27017',maxPoolSize=None)
    db_mon = conn_mongo.python_test #database
    db_collection = db_mon.test_01 #table

    power = 20
    tel = 110
    # 查询
    query_mon = db_collection.find_one({'tel':tel})
    #如果查到号码信息，执行更新
    if query_mon:
        # db_collection.update_one({'tel': tel}, {'$set': {'power': 20}})
        if power == 20:
            select()

    #如果没查到，执行插入号码信息
    else:
        #插入数据
        insert_mon = db_collection.insert_one({'tel':tel,'power':28})
        print('insert---',query_mon)


def select():
    coor = 120.18201
    print(coor)
    return coor

if __name__ == '__main__':
    insert_tel()
