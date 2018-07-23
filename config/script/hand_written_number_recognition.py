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
#   inX:输入向量、手写体识别的测试向量
#   dataSet:训练集样本、手写体识别的训练集向量
#   labels:训练集对应的标签向量
#   k:最近邻居数目、本实验为3
# ---------------------------------------------
def hand_writing_class(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]     # 手写体样本集容量
    # (以下三行)距离计算
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5   # 欧氏距离开平方
    sortedDistIndicies = distances.argsort()  # 距离排序的索引排序
    classCount = {}
    # (以下两行)选择距离最小的k个点
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(),
    # 排序
    key = operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

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
    hand_writing()