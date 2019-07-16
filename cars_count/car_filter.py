import pandas as pd
import jieba

def word_cut(cars):
    return [jieba.lcut(car) for car in cars]

if __name__ == "__main__":
    with open('D:/Project/Code/cars_count/201904.txt', 'r', encoding='utf-8') as fr:
        content = fr.read()

    list_content = [w.strip() for w in content.split('\t\n') if len(w.strip()) != 0]
    tmp = list_content[0].split('\n\n')
    title = tmp[:-1]
    cars = list_content[1:]
    cars[0:0] = [tmp[-1]]
    car_type = set([w.strip() for w in open('D:/Project/Code/cars_count/car_type.txt',encoding='utf-8').readlines()])
    car_info = set([w.strip() for w in open('D:/Project/Code/cars_count/car_info.txt',encoding='utf-8').readlines()])
    jieba.load_userdict('D:/Project/Code/cars_count/car_info.txt')
    jieba.load_userdict('D:/Project/Code/cars_count/car_type.txt')
    cars_cut = word_cut([car.split('\n')[0].strip() for car in cars])
    type_index = [index for index,car_cut in enumerate(cars_cut) if not set(car_cut).isdisjoint(car_type)]
    cars_type = pd.Series(cars).iloc[type_index]
    cars_type_sentences = [i.split('\n') for i in cars_type]

    cars_type_info = []
    for car_type_sentences in cars_type_sentences:
        car_type_sentences_cut = word_cut(car_type_sentences[2:])
        car_type_info = [car_type_sentences[0],car_type_sentences[1]]
        for index,sentence in enumerate(car_type_sentences_cut):
            if not set(sentence).isdisjoint(car_info):
                car_type_info.append(car_type_sentences[index + 2])
        cars_type_info.append(car_type_info)

    with open('D:/Project/Code/cars_count/201904bk.txt','w',encoding='utf-8') as fw:
        txt = '\n\n'.join(title)
        fw.write(txt)
        fw.write('\n\n')
        for i in cars_type_info:
            txt = '\n'.join(i)
            fw.write(txt)
            fw.write('\n\n\n\t\n')