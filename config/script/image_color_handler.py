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


class NewImage:
    def __init__(self, file_name):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.img_file_dir = os.path.join(self.base_dir, u'sample\image_color')
        self.file_dir = os.path.join(self.img_file_dir, file_name)
        self.im = Image.open(self.file_dir)

    @classmethod
    def get_pixel_color(cls, pixel, k=3):
        color_list = [
            # red 1
            [[255, 0, 0], [220, 20, 60], [139, 0, 0], [240, 128, 128]],
            # orange 2
            [[255, 165, 0], [255, 140, 0], [255, 127, 80], [255, 69, 0], [255, 99, 71]],
            # yellow 3
            [[255, 255, 0], [255, 215, 0], [240, 230, 140]],
            # green 4
            [[0, 128, 0], [0, 250, 154], [0, 255, 127], [46, 139, 87], [152, 251, 152], [0, 100, 0], [173, 255, 47]],
            # blue 5
            [[0, 0, 255], [0, 0, 139], [0, 0, 128], [30, 144, 255], [0, 191, 255], [70,130,180]],
            # purple 6
            [[128, 0, 128], [199, 21, 133], [218, 112, 214], [238, 130, 238], [255, 0, 255], [148, 0, 211], [153, 50, 204]],
            # pink 7
            [[255, 192, 203], [255, 182, 193], [219, 112, 147], [255, 105, 180], [255, 20, 147], [218, 112, 214]],
            # brown 8
            [[165, 42, 42], [128, 0, 0], [178, 34, 34], [160, 82, 45], [139, 69, 19]],
            # white 9
            [[255, 255, 255], [245, 245, 245], [220, 220, 220], [211, 211, 211]],
            # black 10
            [[0, 0, 0], [105, 105, 105], [80, 80, 80]]
        ]
        color_range_list = []
        for i, color in enumerate(color_list):
            for color_item in color:
                c_r, c_g, c_b = color_item
                d_r, d_g, d_b = pixel[:3]
                r = math.sqrt(numpy.square((c_r-d_r)) + numpy.square((c_g-d_g)) + numpy.square((c_b-d_b)))
                color_range_list.append([(i+1), int(r)])
        sorted_color_list = sorted(color_range_list, key=lambda x: x[1])
        k_sorted_color_list = sorted_color_list[:k]
        tag_list = [k_color[0] for k_color in k_sorted_color_list]
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
                print u'像素数量： %s' % pixel_count
                tmp_color = 0
                tmp_value = 1
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
    d = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    img_file_dir = os.path.join(d, u'sample\image_color')
    all_file = os.listdir(img_file_dir)
    all_file_count = 0
    test_success_count = 0
    for f in all_file:
        color_type = f.split('_')[0]
        img = NewImage(f)
        if img.im.mode != 'RGBA':
            continue
        all_file_count += 1
        k_color_type = img.get_image_color(z=10)
        print f, color_type, k_color_type
        if int(k_color_type) == int(color_type):
            test_success_count += 1
    print u'检测文件数：%s， 匹配数： %s， 成功率： %s' % (all_file_count,
                                           test_success_count, (float(test_success_count) / float(all_file_count)) * 100)