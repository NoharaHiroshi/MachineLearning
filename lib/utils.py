# encoding=utf-8

from math import log


def cal_shannon_ent(data_set):
    # 数据集的容量
    num = len(data_set)
    # 标签字典
    labels = dict()
    for data in data_set:
        current_label = data[-1]
        if current_label not in labels:
            labels[current_label] = 1
        else:
            labels[current_label] += 1
    # 统计数据集中每个数据项出现的频次
    print labels
    shannon_ent = 0.0
    for key in labels:
        # prob 为当前数据项出现的频率（该数据集出现的概率）
        prob = float(labels[key]) / num
        # 计算熵值
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent


def create_data_set():
    data_set = [[1, 1, 'maybe'],
                [1, 1, 'yes'],
                [1, 0, 'no'],
                [0, 1, 'no'],
                [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return data_set, labels

if __name__ == '__main__':
    d, l = create_data_set()
    s_e = cal_shannon_ent(d)
    print s_e