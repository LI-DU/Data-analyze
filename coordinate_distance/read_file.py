import os
import time
import pandas as pd
import pymongo
from flask import Flask, jsonify,render_template
from datetime import datetime
from math import sin, asin, cos, radians, fabs, sqrt,degrees

EARTH_RADIUS=6371
distance = 5
time_day = datetime.now().strftime('%Y%m%d')   #今天日期

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def power():
    df = pd.read_csv('D:/coordinate/log/2019042810.txt', encoding='utf-8')
    for i in range(len(df)):
        power = df.loc[i][1]
        print(power)
        if power > 30:
            break
        power_data = {'power':power}
        return jsonify(power_data)


if __name__ == '__main__':
    app.run()


