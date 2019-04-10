#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import time
import codecs
import subprocess
import datetime


path = '/home/admin/LOG'
time_day = datetime.now().strftime('%Y%m%d')

#从日志文件中读取数据
def get_file_size(new_file):
    fsize = os.path.getsize(new_file)
    fsize = fsize/float(1024*1024)
    return fsize
 
def get_the_new_file():
    files = os.listdir(path)
    # int_time = int(time_now)
    files_list = list(filter(lambda x:x[-4:]=='.log' and x[0:8]==time_day, files))
    files_list.sort(key=lambda fn:os.path.getmtime(path + '/' + fn) if not os.path.isdir(path + '/' + fn) else 0)
    new_file = os.path.join(path, files_list[-1])
    return new_file
 
def pg_data_to_elk():
    while True:
        new_file = get_the_new_file()
        p = subprocess.Popen('tail -F {0}'.format(new_file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)    #起一个进程，执行shell命令
        while True:
            line = p.stdout.readline()   #实时获取行
            if line:                     #如果行存在的话
                if get_file_size(new_file) > 20:    #如果大于20M，则跳出循环
                    break
        time.sleep(3)

pg_data_to_elk()

#--------------------------------
#linux中实时读取日志
import subprocess
import time

p = subprocess.Popen('tail -F /home/admin/LOG/2019040916.log',shell=True,
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
while True:
    line = p.stdout.readline()
    if line:
        print(line)


