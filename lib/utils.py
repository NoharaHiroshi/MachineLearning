# encoding=utf-8

from math import log


# 主要用来度量数据集的无序程度
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
    shannon_ent = 0.0
    for key in labels:
        # prob 为当前数据项出现的频率（该数据集出现的概率）
        prob = float(labels[key]) / num
        # 计算熵值
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent


def create_data_set():
    # 数据标签越混乱，熵值越高，所有数据集只有一个标签时，熵值为0
    data_set = [[1, 1, 'yes'],
                [1, 1, 'yes'],
                [1, 0, 'no'],
                [0, 1, 'no'],
                [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return data_set, labels


# 这个函数的作用就是把符合条件的数据筛选出来，并返回剩余的特征和标签
def split_data_set(data_set, axis, value):
    ret_data_set = list()
    for feat_vec in data_set:
        if feat_vec[axis] == value:
            reduce_feat_vec = feat_vec[:axis]
            reduce_feat_vec.extend(feat_vec[axis+1:])
            ret_data_set.append(reduce_feat_vec)
    return ret_data_set


def choose_best_feature_to_split(data_set):
    # print u'原始数据集：%s' % data_set
    # 获取数据的特征值个数，-1是标签
    num_features = len(data_set[0]) - 1
    # 计算了整个数据集的原始香农熵，保存最初的无序度量值，用于与划分后的数据集进行熵值的比较
    base_entropy = cal_shannon_ent(data_set)
    # print u'原始香农熵值：%s' % base_entropy
    base_info_gain = 0.0
    # 最利于划分数据的特征，默认-1
    best_feature = -1
    for i in range(num_features):
        # print u'************************当前特征：%s************************' % i
        # 特征值列表
        feat_list = [example[i] for example in data_set]
        # 去重
        unique_values = set(feat_list)
        new_entropy = 0.0
        # 循环标签
        for value in unique_values:
            # print u'——————————————————当前特征值：%s——————————————————————' % value
            sub_data_set = split_data_set(data_set, i, value)
            # print sub_data_set
            # 当前标签出现的概率
            prob = len(sub_data_set) / float(len(data_set))
            shannon_ent = cal_shannon_ent(sub_data_set)
            # 香农熵的数值和样本数量有关
            new_entropy += prob * shannon_ent
        # 划分完一个特征，计算香农熵值是否减少及减少量，减少的越多，越有序
        info_gain = base_entropy - new_entropy
        # print u'香农熵值： %s' % info_gain
        if info_gain > base_info_gain:
            base_info_gain = info_gain
            best_feature = i
    return best_feature


# 返回出现次数最多的值
def majority_cnt(class_list):
    class_count = dict()
    for vote in class_list:
        if vote not in class_count:
            class_count[vote] = 1
        else:
            class_count[vote] += 1
    sorted_class_count = sorted(class_count.items(), key=lambda x: x[-1], reverse=True)
    return sorted_class_count[0][0]


def create_tree(data_set, labels):
    tree = dict()
    # 最优划分的特征索引
    best_feature = choose_best_feature_to_split(data_set)
    # 最优划分的特征标签
    best_feature_label = labels[best_feature]
    tree[best_feature_label] = dict()
    second_tree = tree[best_feature_label]
    # 特征值set
    feature_value_set = set([data[best_feature] for data in data_set])
    # 遍历每一个特征值，计算当前特征值
    for f_v in feature_value_set:
        last_data_set = split_data_set(data_set, best_feature, f_v)
        last_data_label_list = [last_data[-1] for last_data in last_data_set]
        # 当前分支划分的数据集中只有一个标签，则结束
        if len(set(last_data_label_list)) == 1:
            second_tree[f_v] = last_data_label_list[0]
        # 继续划分
        else:
            # 剔除最优划分的特征标签
            labels.remove(best_feature_label)
            _tree = create_tree(last_data_set, labels)
            second_tree[f_v] = _tree
    return tree

if __name__ == '__main__':
    d, l = create_data_set()
    print d, l
    print create_tree(d, l)