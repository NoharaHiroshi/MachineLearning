# encoding=utf-8

import os
import re
import traceback
import contextlib
import ImageFilter
import ImageEnhance
import math
import numpy
from PIL import Image
from math import log


class NewImage:
    def __init__(self, file_name, file_path=None):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.img_file_dir = os.path.join(self.base_dir, file_path) if file_path else os.path.join(self.base_dir, u'sample\image_color')
        self.file_dir = os.path.join(self.img_file_dir, file_name)
        self.im = Image.open(self.file_dir)

    @classmethod
    def get_pixel_color(cls, pixel):
        color_list = [
            # red
            [[255, 0, 0], [220, 20, 60]],
            # orange
            [[255, 165, 0]],
            # yellow
            [[255, 255, 0]],
            # green
            [[0, 128, 0]],
            # blue
            [[0, 0, 255]],
            # purple
            [[128, 0, 128]],
            # pink
            [[255, 192, 203]],
            # brown
            [[165, 42, 42]],
            # white
            [[255, 255, 255]],
            # black
            [[0, 0, 0]]
        ]
        color_range_list = []
        for i, color in enumerate(color_list):
            for color_item in color:
                c_r, c_g, c_b = color_item
                # 适用PNG和JPG
                d_r, d_g, d_b = pixel[:3]
                r = math.sqrt(numpy.square((c_r-d_r)) + numpy.square((c_g-d_g)) + numpy.square((c_b-d_b)))
                color_range_list.append([i, int(r)])
        sorted_color_list = sorted(color_range_list, key=lambda x: x[1])
        print sorted_color_list
        index = sorted_color_list[0][0]
        return index

@contextlib.contextmanager
def open_image(file_name, file_path=None):
    new_im = NewImage(file_name, file_path)
    try:
        yield new_im
    except Exception as e:
        print e
    finally:
        pass


def get_image_color(img_name):
    try:
        with open_image(img_name) as image:
            img = image.im
            width, height = img.size
            for h in range(height):
                for w in range(width):
                    color = img.getpixel((w, h))
    except Exception as e:
        print traceback.format_exc(e)

if __name__ == '__main__':
    print NewImage.get_pixel_color((200, 22, 68))