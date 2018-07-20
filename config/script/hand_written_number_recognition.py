# encoding=utf-8

import os
from PIL import Image
from numpy import *


def img2vector(filename):
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\number_data'])
    full_path = '\\'.join([file_path, filename])
    vector = zeros((1, 1024))
    f = open(full_path)
    for i in range(32):
        line_str = f.readline()
        for j in range(32):
            vector[0, 32*i+j] = int(line_str[j])
    return vector

if __name__ == '__main__':
    ver = img2vector('0_0.txt')
    for i in ver:
        print i
