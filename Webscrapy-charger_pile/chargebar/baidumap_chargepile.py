import requests
import re
import csv
import time
from csv import writer



def BusinessFromBaiduDitu(citycode = '287',key_word='特来点充电站',pageno=1):
    parameter = {
        "querytype" : "con",
        "from": "webmap",
        "c": citycode,  # 城市代码
        "wd": key_word,  # 搜索关键词
        "pn": pageno,  # 页数
        "nn": pageno * 10,
        "db": "0",
        "sug": "0",
        "addr": "0",
        "da_src": "shareurl",
        "on_gel": "1",
        "gr": 3,
        "l": 12,
        "device_ratio": 2,

    }

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ''Chrome/51.0.2704.63 Safari/537.36'}

    url = 'http://map.baidu.com/search/'
    htm = requests.get(url, params=parameter, headers=headers)
    htm = htm.text.encode('latin-1').decode('unicode_escape')  # 转码
    print(',--,,,,----',htm)
    pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
    htm = re.findall(pattern, htm)  # 按段落匹配

    for r in htm:
        pattern = r'(?<=\b"\},"name":").+?(?=")'
        name = re.findall(pattern, r)
        #if not name:
        pattern = r'(?<=\b,"name":").+?(?=")'
        name = re.findall(pattern, r)
        #print(name[0])  # 名称

        pattern = r'.+?(?=")'
        adr = re.findall(pattern, r)
        pattern = r'\(.+?\['
        address = re.sub(pattern, ' ', adr[0])
        pattern = r'\(.+?\]'
        address = re.sub(pattern, ' ', address)
        #print(address)  # 地址

        pattern = r'(?<="phone":").+?(?=")'
        phone = re.findall(pattern, r)
        try:
            if phone[0] and '",' != phone[0]:
                phone_list = phone[0].split(sep=',')
                for number in phone_list:
                    if re.match('1', number):
                        print(citycode+name[0]+','+address+','+number)
                        writer.writerow((name[0], address, number))
        except:
            continue
    print(citycode + '  ' + key_word + '  ' + str(pageno))


# citynumlist是百度地图城市代码列表
citynumlist = ['289', '288', '280']
keywordlist = ['特来电充电站','星星充电站']

start = time.time()
num = 1

#建立csv文件，保存数据
csvFile = open(r'd:/%s.csv' % 'CityData','a+', newline='', encoding='utf-8')
wri = csv.writer(csvFile)
wri.writerow(('name', 'address', 'number'))

if __name__ == '__main__':

    for citycode in citynumlist:
        for kw in keywordlist:
            for page in range(10):
                BusinessFromBaiduDitu(citycode=citycode, key_word=kw, pageno=page)

                #防止访问频率太高，避免被百度公司封
                time.sleep(1)
                if num%20 == 0:
                    time.sleep(2)
                if num%100== 0:
                    time.sleep(3)
                if num%200==0:
                    time.sleep(7)
                num = num + 1

    end = time.time()
    lasttime = int((end-start))
    print('耗时'+str(lasttime)+'s')