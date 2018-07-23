# encoding=utf-8

import os
from PIL import Image
from numpy import *


# 图片转换向量
def img2vector(filename):
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\test'])
    full_path = '\\'.join([file_path, filename])
    # 1行1024列
    vector = zeros((1, 1024))
    f = open(full_path)
    for i in range(32):
        line_str = f.readline()
        for j in range(32):
            vector[0, 32*i+j] = int(line_str[j])
    return vector


# ---------------------------------------------
#   分类模块
#   @params
#   in_x:输入向量、手写体识别的测试向量
#   data_set:训练集样本、手写体识别的训练集向量
#   labels:训练集对应的标签向量
#   k:最近邻居数目、本实验为3
# ---------------------------------------------
def hand_writing_class(in_x, data_set, labels, k):
    # shape函数获取数组的维度
    data_set_size = data_set.shape[0]
    # (以下三行)距离计算
    # tile函数
    # >> > a = [0, 1, 2]
    # >> > b = tile(a, 2)
    # >> > b
    # array([0, 1, 2, 0, 1, 2])
    #
    # >> > b = tile(a, (1, 2))
    # >> > b
    # array([[0, 1, 2, 0, 1, 2]])
    #
    # >> > b = tile(a, (2, 1))
    # >> > b
    # array([[0, 1, 2],
    #        [0, 1, 2]])
    diff_mat = tile(in_x, (data_set_size, 1)) - data_set
    sq_diff_mat = diff_mat**2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances**0.5   # 欧氏距离开平方
    sorted_dist_ind = distances.argsort()  # 距离排序的索引排序
    class_count = {}
    # (以下两行)选择距离最小的k个点
    for i in range(k):
        vote_label = labels[sorted_dist_ind[i]]
        class_count[vote_label] = class_count.get(vote_label, 0) + 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def hand_writing():
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\test'])
    hw_file_list = os.listdir(file_path)
    m = len(hw_file_list)
    for i in range(m):
        file_name_str = hw_file_list[i]
        full_file_path = os.path.join(file_path, file_name_str)
        num_type = file_name_str.split('_')[0]
        f = open(full_file_path)
        f_line = f.readlines()
        for l in f_line:
            l = l.replace('\n', '')
            print l


if __name__ == '__main__':
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\test'])
    name = '0_0.txt'
    sample_name = '0_1.txt'
    full_file_path = os.path.join(file_path, name)
    sample_file_path = os.path.join(file_path, sample_name)
    f = open(full_file_path)
    sample_f = open(sample_file_path)
    in_x = img2vector(f)
    data_set = img2vector(f)
