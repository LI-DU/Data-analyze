#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import time
import codecs
import subprocess
from datetime import datetime
import numpy as np
import pandas as pd


path = '/home/admin/LOG'
time_day = datetime.now().strftime('%Y%m%d')
print(time_day)

#从日志文件中读取数据
def get_file_size(new_file):
    fsize = os.path.getsize(new_file)
    fsize = fsize/float(1024*1024)  #file size, M
    return fsize
 
def get_the_new_file():
    files = os.listdir(path)
    files_list = list(filter(lambda x:x[-4:]=='.log' and x[0:8]==time_day, files))
    files_list.sort(key=lambda fn:os.path.getmtime(path + '/' + fn) if not os.path.isdir(path + '/' + fn) else 0)
    new_file = os.path.join(path, files_list[-1])
    return new_file
 
def tail_cor_log():
    while True:
        new_file = get_the_new_file()
        p = subprocess.Popen('tail -f {0}'.format(new_file), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)    #起一个进程，执行shell命令
        print(type(p))
        while True:
            line = p.stdout.readline()   #实时获取行
            if line:                     #如果行存在的话
                if get_file_size(new_file) > 20:    #如果大于20M，则跳出循环
                    break

            line_dec = line.decode()
            split_line = line_dec.split()
            print('------------------')
            pd_line = pd.DataFrame(split_line)
#             pd_line = pd.DataFrame([line_dec])
#             print(pd_line)
            print(float(pd_line.loc[2]))
    
            res2 = pd_line.loc[2] - 120.003451
            print(res2)

        time.sleep(0.5)

if __name__ == '__main__':
    tail_cor_log()
