# encoding=utf-8

import os
from PIL import Image
from numpy import *


# 图片转换向量
def img2vector(filename):
    # 1行1024列
    vector = zeros((1, 1024))
    f = open(filename)
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
    # ** 代表指数运算
    sq_diff_mat = diff_mat**2
    # c = np.array([[0, 2, 1], [3, 5, 6], [0, 1, 1]])
    # print c.sum()
    # print c.sum(axis=0)
    # print c.sum(axis=1)
    # 结果分别是：19, [3 8 8], [ 3 14  2]
    # axis=0, 表示列。
    # axis=1, 表示行。
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
    training_mat = zeros([0, 1024])
    labels = list()
    for i in range(m):
        file_name_str = hw_file_list[i]
        full_file_path = os.path.join(file_path, file_name_str)
        num_type = file_name_str.split('_')[0]
        labels.append(num_type)
        vector = img2vector(full_file_path)
        training_mat[i, :] = vector
    test_file_path = '\\'.join([base_dir, r'sample\number_data'])
    test_file_list = os.listdir(test_file_path)
    error_count = 0.0
    m_test = len(test_file_list)
    for i in range(m_test):
        test_file_name_str = test_file_list[i]
        test_full_file_path = os.path.join(file_path, test_file_name_str)
        test_num_type = test_file_name_str.split('_')[0]
        test_vector = img2vector(test_full_file_path)
        classify_result = hand_writing_class(test_vector, training_mat, labels, 3)
        print 'the classify result is %s, the real answer is %s' % (classify_result, test_num_type)
        if classify_result != test_num_type:
            error_count += 1.0
        print error_count

if __name__ == '__main__':
    hand_writing()

