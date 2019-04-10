#!/usr/bin/env python

import time
import os
import re

#每秒写入一行数据
def seconds_write():
    n = 0
    while n < 1000:
        with open('/home/admin/LOG/2019040916.log','a+') as f:
            f.write('cn010 31.148974 120.65263'+ '\n')
            time.sleep(1)
        n += 1
seconds_write()

