import pymongo

# 配置数据库信息
mongo_host = 'localhost'
mongo_db = 'python_test' # 数据库名
mongo_tb = 'python_test' # 表名

# 连接数据库
client = pymongo.MongoClient(mongo_host)
db = client[mongo_db]

# 存入数据库
def save_url_to_Mongo(data):
    try:
        if db[mongo_tb].find_one(data):
            print('有此条数据', data)
            db[mongo_tb].update_one(data)
        else:
            print('之前没有此条数据', data)
            db[mongo_tb].insert(data)
    except Exception:
        print('存储到MongoDb失败')

data = {'num':1234}
save_url_to_Mongo(data)


