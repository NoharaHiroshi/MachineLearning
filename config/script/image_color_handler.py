# encoding=utf-8

import os
import re
import traceback
import contextlib
import ImageFilter
import ImageEnhance
import time
import math
import numpy
from PIL import Image
from math import log

DEBUG = False

class NewImage:
    def __init__(self, file_name):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.img_file_dir = os.path.join(self.base_dir, r'sample\test_image_color')
        self.file_dir = os.path.join(self.img_file_dir, file_name)
        self.im = Image.open(self.file_dir)

    @classmethod
    def get_pixel_color(cls, pixel, k=3):
        color_list = [
            # red 1
            [[255, 0, 0], [172, 18, 44], [191, 50, 47]],
            # orange 2
            [[255, 165, 0], [236, 102, 58]],
            # yellow 3
            [[255, 255, 0], [255, 196, 125], [255, 224, 184], [252, 207, 0], [252, 221, 170]],
            # green 4
            [[0, 255, 0], [86, 130, 84], [68, 118, 54], [236, 241, 179], [236, 241, 179], [236, 241, 178], [166, 208, 111], [146, 195, 6], [140, 186, 0]],
            # blue 5
            [[0, 0, 255], [26, 191, 229], [15, 65, 134], [7, 80, 144], [83, 197, 238], [121, 145, 154]],
            # purple 6
            [[160, 32, 240], [83, 90, 168], [102, 110, 181], [97, 117, 182], [122, 135, 200], [72, 80, 147], [171, 116, 149], [138, 24, 107], [178, 3, 120]],
            # pink 7
            [[255, 192, 203], [255, 216, 195], [249, 129, 155]],
            # brown 8
            [[165, 42, 42], [121, 100, 93], [199, 150, 59], [192, 131, 31]],
            # white 9
            [[255, 255, 255], [239, 242, 242], [198, 198, 198], [251, 145, 164], [186, 110, 22]],
            # black 10
            [[0, 0, 0]],
            # chin 11
            [[144, 233, 213], [37, 175, 144], [128, 214, 200], [145, 234, 214], [51, 212, 200], [10, 132, 125]],
        ]
        color_range_list = []
        for i, color in enumerate(color_list):
            for color_item in color:
                c_r, c_g, c_b = color_item
                d_r, d_g, d_b = pixel[:3]
                r = math.sqrt(numpy.square((c_r-d_r)) + numpy.square((c_g-d_g)) + numpy.square((c_b-d_b)))
                color_range_list.append([color_item, pixel[:3], (i+1), int(r)])
        sorted_color_list = sorted(color_range_list, key=lambda x: x[-1])
        if DEBUG:
            print sorted_color_list
        k_sorted_color_list = sorted_color_list[:k]
        # print sorted_color_list
        tag_list = [k_color[-2] for k_color in k_sorted_color_list]
        # 空白tag
        tmp_tag = tag_list[0]
        # 最大出现次数
        tmp_max_num = 1
        for tag in tag_list:
            if tag_list.count(tag) > tmp_max_num:
                tmp_max_num = tag_list.count(tag)
                tmp_tag = tag
        return tmp_tag

    def get_image_color(self, z=5):
        # 参数z代表压缩级别
        try:
            img = self.im
            if img.mode == 'RGBA':
                width, height = img.size
                start = time.time()
                color_record_dict = dict()
                pixel_count = 0
                for h in range(0, height, z):
                    for w in range(0, width, z):
                        pixel_count += 1
                        color = img.getpixel((w, h))
                        # 透明通道不在统计范围内
                        if color[-1] > 250:
                            tag = NewImage.get_pixel_color(color)
                            if tag not in color_record_dict:
                                color_record_dict[tag] = 1
                            else:
                                color_record_dict[tag] += 1
                            if DEBUG:
                                print color, tag
                print u'像素数量： %s' % pixel_count
                tmp_color = 0
                tmp_value = 1
                if DEBUG:
                    print color_record_dict
                for k, v in color_record_dict.items():
                    if v > tmp_value:
                        tmp_color = k
                        tmp_value = v
                end = time.time()
                print u'当前用时： %s s' % float((end - start))
                return tmp_color
            else:
                return 0
        except Exception as e:
            print traceback.format_exc(e)


@contextlib.contextmanager
def open_image(file_name):
    new_im = NewImage(file_name)
    try:
        yield new_im
    except Exception as e:
        print e
    finally:
        pass

if __name__ == '__main__':
    # 记录
    # 第一次测试： 检测文件数72，匹配率30， 准确率41.6%
    # 第二次测试： 检测文件数72，匹配率31， 准确率43.0%， 压缩了检测像素点的数量，提高了速度
    # 分别测试了压缩率5， 10， 20，当前样本规模差别不大
    # 第三次测试： 检测文件数83， 匹配数55， 准确率66.2%， 各结果样本数量基本一致，是影响k-近邻算法准确性的重要因素，已基本符合判断，毕竟颜色并不是准确的值

    # d = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # img_file_dir = os.path.join(d, u'sample\image_color')
    # all_file = os.listdir(img_file_dir)
    # all_file_count = 0
    # test_success_count = 0
    # for f in all_file:
    #     color_type = f.split('_')[0]
    #     img = NewImage(f)
    #     if img.im.mode != 'RGBA':
    #         continue
    #     all_file_count += 1
    #     k_color_type = img.get_image_color(z=10)
    #     print f, color_type, k_color_type
    #     if int(k_color_type) == int(color_type):
    #         test_success_count += 1
    # print u'检测文件数：%s， 匹配数： %s， 成功率： %s' % (all_file_count,
    #                                        test_success_count, (float(test_success_count) / float(all_file_count)) * 100)

    # DEBUG = True
    # img = NewImage('5_5_4_4_4_4_290e2b2f8869ec7e9ed09d595c27956e.png')
    # img.get_image_color(z=10)

    d = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    img_file_dir = os.path.join(d, r'sample\test_image_color')
    all_file = os.listdir(img_file_dir)
    for f in all_file:
        img = NewImage(f)
        if img.im.mode != 'RGBA':
            continue
        k_color_type = img.get_image_color(z=10)
        new_file_name = '%s_%s' %(str(k_color_type), f)
        old_file = os.path.join(img_file_dir, f)
        new_file = os.path.join(img_file_dir, new_file_name)
        os.rename(old_file, new_file)
