#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache Software License
import json
import os
import time
from typing import List
from xmlrpc.client import Binary
from xmlrpc.client import ServerProxy

try:
    import easyprocess
    import pyscreenshot

    PYSCREENSHOT = True
except ImportError:
    PYSCREENSHOT = False
from funnylog2 import logger

from pylinuxauto.config import config


class OCRBase:
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
        return f"http://{config.OCR_SERVER_IP}:{config.OCR_PORT}"

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
    def _pdocr_client(
            cls,
            lang,
            picture_abspath: str = None,
            screen_bbox: List[int] = None,
            network_retry: int = 1
    ):
        """
         通过 RPC 协议进行 OCR 识别。
        :return: 返回 PaddleOCR 的原始数据
        """
        # 截全屏
        if picture_abspath is None:
            if screen_bbox:
                fullscreen_path = os.popen(cls.screenshot_area_dbus(*screen_bbox)).read().strip().strip("\n")
            else:
                if PYSCREENSHOT:
                    fullscreen_path = config.SCREEN_CACHE
                    try:
                        pyscreenshot.grab().save(os.path.expanduser(fullscreen_path))
                    except easyprocess.EasyProcessError:
                        ...
                else:
                    fullscreen_path = os.popen(cls.screenshot_fullscreen_dbus()).read().strip().strip("\n")
        else:
            fullscreen_path = picture_abspath

        put_handle = open(os.path.expanduser(fullscreen_path), "rb")
        for _ in range(network_retry + 1):
            try:
                # 将图片上传到服务端
                pic_dir = cls.server().image_put(Binary(put_handle.read()))
                put_handle.close()
                # 返回识别结果
                logger.info(f"USE_OCR_SERVER http://{config.OCR_SERVER_IP}")
                pic_path = cls.server().paddle_ocr(pic_dir, lang)
                return pic_path
            except OSError:
                continue
        raise EnvironmentError(
            f"OCR_SERVER访问失败 {cls.server_url()}"
        )

    @classmethod
    def _ocr(
            cls,
            *target_strings: str,
            picture_abspath: str = None,
            screen_bbox: List[int] = None,
            similarity: [float, int] = 0.6,
            return_default: bool = False,
            return_first: bool = False,
            lang: str = "ch",
            network_retry: int = 1,
    ):
        """
         通过 OCR 进行识别。
        :param target_strings:
            目标字符,识别一个字符串或多个字符串,并返回其在图片中的坐标;
            如果不传参，返回图片中识别到的所有字符串。
        :param picture_abspath: 要识别的图片路径，如果不传默认截取全屏识别。
        :param similarity: 匹配度。
        :param return_default: 返回识别的原生数据。
        :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
        :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
        :param retry: 连接服务器重试次数
        :return: 返回的坐标是目标字符串所在行的中心坐标。
        """
        results = cls._pdocr_client(
            picture_abspath=picture_abspath,
            lang=lang,
            screen_bbox=screen_bbox,
            network_retry=network_retry
        )
        if return_default:
            return results
        more_map = {}
        if len(target_strings) == 1:
            n = 1
            for res in results[0]:
                try:
                    [
                        [
                            [left_top_x, left_top_y],
                            [right_top_x, right_top_y],
                            [right_bottom_x, right_bottom_y],
                            [left_bottom_x, left_bottom_y],
                        ],
                        [strings, rate],
                    ] = res
                except ValueError as e:
                    print(res)
                    raise ValueError(e) from e
                if target_strings[0] in strings:
                    if rate >= similarity:
                        center_x = (right_top_x + left_top_x) / 2
                        center_y = (right_bottom_y + right_top_y) / 2
                        more_map[
                            target_strings[0]
                            if not more_map.get(target_strings[0])
                            else f"{target_strings[0]}_{n}"
                        ] = (center_x, center_y)
                        if return_first:
                            break
                        n += 1
            if len(more_map) == 1:
                center_x, center_y = more_map.get(target_strings[0])
                logger.debug(f"OCR识别到字符 [{target_strings[0]}]—>{center_x, center_y}")
                return center_x, center_y
            if len(more_map) > 1:
                logger.debug(f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}")
                return more_map

        elif len(target_strings) == 0:
            for res in results[0]:
                [
                    [
                        [left_top_x, left_top_y],
                        [right_top_x, right_top_y],
                        [right_bottom_x, right_bottom_y],
                        [left_bottom_x, left_bottom_y],
                    ],
                    (strings, rate),
                ] = res
                if rate >= similarity:
                    center_x = (right_top_x + left_top_x) / 2
                    center_y = (right_bottom_y + right_top_y) / 2
                    more_map[strings] = (center_x, center_y)

            if more_map:
                logger.debug(f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}")
                return more_map

        else:
            for target_string in target_strings:
                n = 1
                more_map[target_string] = False
                for res in results[0]:
                    [
                        [
                            [left_top_x, left_top_y],
                            [right_top_x, right_top_y],
                            [right_bottom_x, right_bottom_y],
                            [left_bottom_x, left_bottom_y],
                        ],
                        (strings, rate),
                    ] = res
                    if target_string in strings and rate >= similarity:
                        center_x = (right_top_x + left_top_x) / 2
                        center_y = (left_bottom_y + left_top_y) / 2
                        if more_map.get(target_string):
                            _key = f"{target_string}_{n}"
                        else:
                            _key = target_string
                            n = 1
                        more_map[_key] = (center_x, center_y)
                        if return_first:
                            break
                        n += 1

            if more_map:
                logger.debug(f"OCR识别结果:\n{json.dumps(more_map, ensure_ascii=False, indent=2)}")
                return more_map
        res_log = []
        for res in results[0]:
            [[*_], [strings, rate]] = res
            res_log.append(strings)
        logger.debug(f"未识别到字符{target_strings}, 识别到的原始内容：{res_log}")
        return False

    @classmethod
    def ocr(
            cls,
            *target_strings,
            picture_abspath: str = None,
            similarity: [int, float] = 0.6,
            return_default: bool = False,
            return_first: bool = False,
            lang: str = "ch",
            network_retry: int = None,
            pause: [int, float] = None,
            timeout: [int, float] = None,
            max_match_number: int = None,
    ):
        """
        通过 OCR 进行识别。
        :param target_strings:
            目标字符,识别一个字符串或多个字符串,并返回其在图片中的坐标;
            如果不传参，返回图片中识别到的所有字符串。
        :param picture_abspath: 要识别的图片路径，如果不传默认截取全屏识别。
        :param similarity: 匹配度。
        :param return_default: 返回识别的原生数据。
        :param return_first: 只返回第一个,默认为 False,返回识别到的所有数据。
        :param lang: `ch`, `en`, `fr`, `german`, `korean`, `japan`
        :param network_retry: 连接服务器重试次数
        :param pause: 重试间隔时间,单位秒
        :param timeout: 最大匹配超时,单位秒
        :param max_match_number: 最大匹配次数
        :return: 返回的坐标是目标字符串所在行的中心坐标。
        """
        network_retry = network_retry if network_retry else config.OCR_NETWORK_RETRY
        pause = pause if pause else config.OCR_PAUSE
        timeout = timeout if timeout else config.OCR_TIMEOUT
        max_match_number = max_match_number if max_match_number else config.OCR_MAX_MATCH_NUMBER
        ignore_time = 0
        start = time.time()
        for _ in range(max_match_number):
            end = time.time()
            during = end - start - ignore_time
            if during > timeout:
                return False
            _start = time.time()
            res = cls._ocr(
                *target_strings,
                picture_abspath=picture_abspath,
                similarity=similarity,
                return_default=return_default,
                return_first=return_first,
                lang=lang,
                network_retry=network_retry,
            )
            _end = time.time()
            ignore_time += (_end - _start)
            if res is False:
                time.sleep(pause)
                continue
            return res
        return False
