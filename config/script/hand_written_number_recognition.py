# encoding=utf-8

import os
from PIL import Image
from numpy import *


# 图片转换向量
def img2vector(filename):
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\number_data'])
    full_path = '\\'.join([file_path, filename])
    # 1行1024列
    vector = zeros((1, 1024))
    f = open(full_path)
    for i in range(32):
        line_str = f.readline()
        for j in range(32):
            vector[0, 32*i+j] = int(line_str[j])
    return vector


def hand_writing():
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\number_data'])
    hw_file_list = os.listdir(file_path)
    m = len(hw_file_list)
    for i in range(m):
        file_name_str = hw_file_list[i]
        num_type = file_name_str.split('_')[0]
        vector = img2vector(file_name_str)
        print vector


if __name__ == '__main__':
    pass