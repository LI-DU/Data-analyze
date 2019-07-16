import os

#获得用户的点击序列
def get_user_click(rating_file):
    if not os.path.exists(rating_file):
        return {}

    #打开文件
    fp = open(rating_file)
    num = 0

    #用于传回文件
    user_click = {}
    for line in fp:
        #第一行是columns名称，需要跳过处理
        if num == 0:
            num += 1
            continue



