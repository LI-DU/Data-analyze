import os
import time
from flask import Flask, jsonify,render_template
from datetime import datetime
from math import sin, asin, cos, radians, fabs, sqrt,degrees

EARTH_RADIUS=6371
distance = 5
time_day = datetime.now().strftime('%Y%m%d')   #今天日期

app = Flask(__name__)

# coordinate = ['na001',120.3201,30.287]
path = 'D:/coordinate/log/'

# 获取日志文件大小
def get_file_size(new_file):
    fsize = os.path.getsize(new_file)
    fsize = fsize / float(1024 * 1024)  # 计算日志文件大小，以M为单位
    return fsize


# 获取当天最新生成的日志文件
def get_the_new_file():
    files = os.listdir(path)
    files_list = list(filter(lambda x: x[-4:] == '.log' and x[0:8] == time_day, files))  # 列出当前目录下今天的日志文件
    files_list.sort(key=lambda fn: os.path.getmtime(path + '/' + fn) if not os.path.isdir(path + '/' + fn) else 0)
    new_file = os.path.join(path, files_list[-1])  # 汇总今天生成的日志，并取最新生成的日志返回
    return new_file


# 读取日志文件，
def tail_cor_log():
    with open('D:/coordinate/log/2019042719.txt',encoding='utf-8') as f:
        p = f.readlines()
        for i in range(len(p)):
            coordinate = p[i]
        return coordinate


def log(rescoor):
    def cor_areas():
        dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(coordinate[1]))
        dlng = degrees(dlng)  # 弧度转换成角度

        # 计算坐标点周围5km，南北两侧距离坐标
        dlat = distance / EARTH_RADIUS
        dlat = degrees(dlat)  # 弧度转换成角度

        # cor1左上角坐标点，cor2右下角坐标点
        cor1_lat, cor1_lng = coordinate[1] + dlat, coordinate[2] - dlng
        cor2_lat, cor2_lng = coordinate[1] - dlat, coordinate[2] + dlng

        return rescoor(cor1_lat, cor1_lng, cor2_lat, cor2_lng)
    return cor_areas

'''
def log(demo):
    def wrapper():
        print('这是在wrapper内部执行的')
        return demo({'lat':30.225})
    return wrapper
'''


@app.route('/', methods=['POST', 'GET'])
@log
def test_file(cor1_lat, cor1_lng, cor2_lat, cor2_lng):
    print('test_file函数内部开始执行',cor1_lat, cor1_lng, cor2_lat, cor2_lng)
    coor = {'lat':30.225,'lng':120.8301}
    return jsonify(coor)

if __name__ == '__main__':
    app.run()


