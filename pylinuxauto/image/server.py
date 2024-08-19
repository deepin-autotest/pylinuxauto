#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache Software License

"""
sudo apt install python3-opencv
"""

import os
from socketserver import ThreadingMixIn
from time import time
from xmlrpc.server import SimpleXMLRPCServer

import cv2 as cv
import numpy as np


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


def check_connected():
    return True


def image_put(data):
    CURRENT_DIR = os.path.abspath(".")
    pic_dir = os.path.join(CURRENT_DIR, "pic")
    if not os.path.exists(pic_dir):
        os.makedirs(pic_dir)

    pic_path = os.path.join(pic_dir, f'pic_{time()}.png')
    handle = open(pic_path, "wb")
    handle.write(data.data)
    handle.close()
    return pic_path


def match_image_by_opencv(template_path, source_path, rate=None, multiple=False):
    """
     图像识别，匹配小图在屏幕中的坐标 x, y
    :param image_path: 图像识别目标文件的存放路径
    :param rate: 匹配度
    :param multiple: 是否返回匹配到的多个目标
    :return: 根据匹配度返回坐标
    """
    template = cv.imread(template_path)
    source = cv.imread(source_path)
    result = cv.matchTemplate(source, template, cv.TM_CCOEFF_NORMED)
    if not multiple:
        pos_start = cv.minMaxLoc(result)[3]
        _x = int(pos_start[0]) + int(template.shape[1] / 2)
        _y = int(pos_start[1]) + int(template.shape[0] / 2)
        similarity = cv.minMaxLoc(result)[1]
        if similarity < rate:
            return False
        return _x, _y
    else:
        loc = np.where(result >= rate)
        tmp_list_out = []
        tmp_list_in = []
        loc_list = list(zip(*loc))
        for i in range(0, len(loc_list) - 1):
            tmp_list_in.append(loc_list[i])
            if (
                    loc_list[i + 1][0] != loc_list[i][0]
                    or (loc_list[i + 1][1] - loc_list[i][1]) > 1
            ):
                tmp_list_out.append(tmp_list_in)
                tmp_list_in = []
                continue
            if i == len(loc_list) - 2:
                tmp_list_in.append(loc_list[-1])
                tmp_list_out.append(tmp_list_in)
        result_list = []
        x_list, y_list = [], []
        if tmp_list_out:
            for i in tmp_list_out:
                for j in i:
                    x_list.append(j[1])
                    y_list.append(j[0])
                x = np.mean(x_list) + int(template.shape[1] / 2)
                y = np.mean(y_list) + int(template.shape[0] / 2)
                result_list.append((x, y))
                x_list, y_list = [], []
            result_list.sort(key=lambda x: x[0])
            return result_list
        return False


def server():
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from pylinuxauto.config import config
    server = ThreadXMLRPCServer(("0.0.0.0", config.IMAGE_PORT), allow_none=True)
    server.register_function(check_connected, "check_connected")
    server.register_function(image_put, "image_put")
    server.register_function(match_image_by_opencv, "match_image_by_opencv")
    print(f"监听客户端请求... {server.server_address}")
    server.serve_forever()


if __name__ == '__main__':
    server()
