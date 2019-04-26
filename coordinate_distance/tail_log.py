#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""从坐标日志文件中实时读取日志内容，输出坐标经纬度"""

import os
import re
import time
import codecs
import subprocess
from datetime import datetime
import numpy as np
import pandas as pd


time_day = datetime.now().strftime('%Y%m%d')

#获取日志文件大小
def get_file_size(new_file):
    fsize = os.path.getsize(new_file)
    fsize = fsize/float(1024*1024)    #计算日志文件大小，以M为单位
    return fsize

#获取当天最新生成的日志文件
def get_the_new_file():
    files = os.listdir(path)
    files_list = list(filter(lambda x:x[-4:]=='.log' and x[0:8]==time_day, files))    #列出当前目录下当天的日志文件
    files_list.sort(key=lambda fn:os.path.getmtime(path + '/' + fn) if not os.path.isdir(path + '/' + fn) else 0)
    new_file = os.path.join(path, files_list[-1])    #汇总当天生成的日志，并取最新生成的日志返回
    return new_file

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
                
                vin = (pd_line.loc[0]
                lat = float(pd_line.loc[1])           #取坐标数据的纬度
                lng = float(pd_line.loc[2])  

        time.sleep(0.5)

if __name__ == '__main__':
    path = '/home/admin/LOG'
    tail_cor_log()