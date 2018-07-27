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


def file2vector(file_path):
    f = open(file_path)
    f_lines = f.readlines()
    f_len = len(f_lines)
    vector = zeros((f_len, f_len))
    for i, line in enumerate(f_lines):
        line = line.replace('\n', '')
        for j, num in enumerate(line):
            vector[(i, j)] = num
    return vector


def get_sample_list():
    sample_data_list = list()
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample/number_data'])
    sample_list = os.listdir(file_path)
    for sample_name in sample_list:
        sample_full_name = os.path.join(file_path, sample_name)
        num_type = sample_name.split('_')[0]
        vector = file2vector(sample_full_name)
        sample_data_list.append([vector, num_type])
    return sample_data_list


def my_hand_writing(data_list, k=3):
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\test'])
    data_data_list = os.listdir(file_path)
    for data_name in data_data_list:
        data_full_name = os.path.join(file_path, data_name)
        num_type = data_name.split('_')[0]
        vector = file2vector(data_full_name)
        result_list = list()
        for data in data_list:
            # 向量欧式距离
            distances = sqrt(sum(square(vector - data[0])))
            result_list.append([data[1], distances])
        result_list = sorted(result_list, key=lambda x: x[1])[:k]
        _result_list = [result[0] for result in result_list]
        result_set = set(_result_list)
        # 最大出现次数
        tmp_max_num = 1
        result = result_list[0][0]
        if len(result_set) != len(_result_list):
            for r in _result_list:
                t_num = _result_list.count(r)
                if t_num > tmp_max_num:
                    tmp_max_num = t_num
                    result = r
        else:
            result = result_list[0][0]
        print u'当前文件: %s, 识别为： %s' % (data_name, result)


# 转换文本查看图片
def hand_writing_handler():
    weight_list = [u'▏', u'▎', u'▍', u'▌', u'▋', u'▊', u'▉', u'█']
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\hand_number'])
    data_data_list = os.listdir(file_path)
    for data in data_data_list:
        full_file_path = os.path.join(file_path, data)
        im = Image.open(full_file_path)
        _im = im.convert('L')
        width, height = _im.size
        w = 100
        h = 100
        _im = _im.resize((w, h))
        for _h in range(h):
            row = list()
            for _w in range(w):
                color = _im.getpixel((_w, _h))
                color_weight = int(color // int(255 // len(weight_list)))
                text_color = weight_list[color_weight]
                row.append(text_color)
            color_str = ''.join(row)
            print color_str


# 清除图片杂乱信息，获取图片内容
def clean_hand_writing_img(img_file):
    base_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:2])
    file_path = '\\'.join([base_dir, r'sample\hand_number'])
    full_file_path = os.path.join(file_path, img_file)
    im = Image.open(full_file_path)
    _im = im.convert('L')
    w = 100
    h = 100
    _im = _im.resize((w, h))
    width, height = _im.size
    color_dict = dict()
    for h in range(height):
        row = list()
        for w in range(width):
            color = _im.getpixel((w, h))
            row.append(str(color))
            if color not in color_dict:
                color_dict[color] = 1
            else:
                color_dict[color] += 1
        color_str = ' '.join(row)
    # 对污染像素进行清洗
    color_dirty_color = sorted(color_dict.items(), key=lambda x: x[1], reverse=True)
    print color_dirty_color


if __name__ == '__main__':
    # d_list = get_sample_list()
    # my_hand_writing(d_list)
    # hand_writing_handler()
    clean_hand_writing_img('2.jpg')
