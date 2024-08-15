#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache Software License
import os
import time
from typing import List, Union
from xmlrpc.client import Binary
from xmlrpc.client import ServerProxy

try:
    import easyprocess
    import pyscreenshot

    PYSCREENSHOT = True
except ImportError:
    PYSCREENSHOT = False
from funnylog2 import logger
from pylinuxauto import exceptions
from pylinuxauto.config import config


class ImageBase:

    @classmethod
    def screenshot_cmd(cls):
        return "dbus-send --session --print-reply=literal --dest=org.kde.KWin /Screenshot org.kde.kwin.Screenshot"

    @classmethod
    def screenshot_fullscreen_dbus(cls):
        return f"{cls.screenshot_cmd()}.screenshotFullscreen"

    @classmethod
    def screenshot_area_dbus(cls, x, y, w, h):
        return f"{cls.screenshot_cmd()}.screenshotArea int32:{x} int32:{y} int32:{w} int32:{h}"


    @classmethod
    def server_url(cls):
        return f"http://{config.IMAGE_SERVER_IP}:{config.IMAGE_PORT}"

    @classmethod
    def server(cls):
        return ServerProxy(cls.server_url(), allow_none=True)

    @classmethod
    def check_connected(cls):
        try:
            return cls.server().check_connected()
        except OSError:
            return False

    @classmethod
    def _match_image_by_opencv(
            cls,
            image_path: str,
            rate: float = None,
            multiple: bool = False,
            picture_abspath: str = None,
            screen_bbox: List[int] = None,
            network_retry: int = 1,
    ):
        """
         图像识别，匹配小图在屏幕中的坐标 x, y，当前仅支持1个主屏幕，如果存在多个屏幕只会截取主屏幕内容。
        :param image_path: 图像识别目标文件的存放路径,仅支持英文文件名，不支持中文文件名
        :param rate: 匹配度
        :param multiple: 是否返回匹配到的多个目标
        :param picture_abspath: 大图，默认大图是截取屏幕，否则使用传入的图片；
        :param screen_bbox: 截取屏幕上指定区域图片（仅支持X11下使用）；
            [x, y, w, h]
            x: 左上角横坐标；y: 左上角纵坐标；w: 宽度；h: 高度；根据匹配度返回坐标
        :param network_retry: 连接服务器重试次数
        """
        if rate is None:
            rate = float(config.IMAGE_RATE)

        # 截全屏
        if picture_abspath is None:
            if screen_bbox:
                fullscreen_path = os.popen(cls.screenshot_area_dbus(*screen_bbox)).read().strip().strip("\n")
            else:
                if PYSCREENSHOT:
                    fullscreen_path = config.SCREEN_CACHE
                    try:
                        pyscreenshot.grab().save(fullscreen_path)
                    except easyprocess.EasyProcessError:
                        ...
                else:
                    fullscreen_path = os.popen(cls.screenshot_fullscreen_dbus()).read().strip().strip("\n")
        # 指定图片
        else:
            fullscreen_path = picture_abspath

        template_path = ""
        image_path = os.path.expanduser(image_path)
        # 如果传入的image_path参数不带文件后缀名，就根据文件类型判断文件是否存在，存在则将后缀类型（'.png','.jpg','.jpeg'）加上
        if not image_path.endswith(('.png', '.jpg', '.jpeg')):
            if os.path.exists(f"{image_path}.png"):
                template_path = f"{image_path}.png"
            elif os.path.exists(f"{image_path}.jpg"):
                template_path = f"{image_path}.jpg"
            elif os.path.exists(f"{image_path}.jpeg"):
                template_path = f"{image_path}.jpeg"
            else:
                logger.error(f"The image format is not supported. Please confirm your image_path again")
        else:
            # image_path参数带有后缀名，不做任何添加
            template_path = image_path
        if not template_path:
            raise ValueError
        screen_rb = open(fullscreen_path, "rb")
        template_rb = open(template_path, "rb")
        for _ in range(network_retry + 1):
            try:
                screen_path = cls.server().image_put(Binary(screen_rb.read()))
                screen_rb.close()
                tpl_path = cls.server().image_put(Binary(template_rb.read()))
                template_rb.close()
                logger.info(f"USE_IMAGE_SERVER http://{config.IMAGE_SERVER_IP}")
                return cls.server().match_image_by_opencv(
                    tpl_path, screen_path, rate, multiple
                )
            except OSError:
                continue
        raise EnvironmentError(
            f"IMAGE_SERVER访问失败 {cls.server_url()}"
        )

    @classmethod
    def find_element(
            cls,
            *widget,
            rate: Union[float, int] = None,
            multiple: bool = False,
            picture_abspath: str = None,
            screen_bbox: List[int] = None,
            network_retry: int = None,
            pause: [int, float] = None,
            timeout: [int, float] = None,
            max_match_number: int = None,
    ):
        """
         在屏幕中区寻找小图，返回坐标，
         如果找不到，根据配置重试次数，每次间隔1秒
        :param picture_abspath:
        :param widget: 模板图片路径
        :param rate: 相似度
        :param multiple: 是否返回匹配到的多个目标
        :param screen_bbox: 截取屏幕上指定区域图片（仅支持X11下使用）；
            [x, y, w, h]
            x: 左上角横坐标；y: 左上角纵坐标；w: 宽度；h: 高度；根据匹配度返回坐标
        :param log_level: 日志级别
        :param network_retry: 连接服务器重试次数
        :param pause: 图像识别重试的间隔时间
        :param timeout: 最大匹配超时,单位秒
        :param max_match_number: 最大匹配次数
        :return: 坐标元组
        """
        network_retry = network_retry if network_retry else config.IMAGE_NETWORK_RETRY
        pause = pause if pause else config.IMAGE_PAUSE
        timeout = timeout if timeout else config.IMAGE_TIMEOUT
        max_match_number = max_match_number if max_match_number else config.IMAGE_MAX_MATCH_NUMBER

        retry_number = int(max_match_number)
        if retry_number < 0:
            raise ValueError("重试次数不能小于0")

        if rate is None:
            rate = float(config.IMAGE_RATE)
        try:
            for element in widget:
                start_time = time.time()
                for _ in range(retry_number + 1):
                    locate = cls._match_image_by_opencv(
                        element,
                        rate,
                        multiple=multiple,
                        picture_abspath=picture_abspath,
                        screen_bbox=screen_bbox,
                        network_retry=network_retry,
                    )
                    if not locate:
                        time.sleep(int(pause))
                    else:
                        return locate
                    end_time = time.time()
                    if end_time - start_time > timeout:
                        break
            raise exceptions.TemplateElementNotFound(*widget)
        except Exception as exc:
            raise exc
