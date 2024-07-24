#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: Apache Software License
import random
from typing import List

from pylinuxauto.config import config
from pylinuxauto.image.image_base import ImageBase
from pylinuxauto.mousekey.mkmixin import MouseKeyChainMixin


class Image(MouseKeyChainMixin):

    @property
    def _image_servers(self) -> List[str]:
        return [i.strip() for i in config.IMAGE_SERVER_IP.split("/") if i]

    def find_element_by_image(self, *args, **kwargs):
        log_server = servers = self._image_servers
        while servers:
            config.IMAGE_SERVER_IP = random.choice(servers)
            if ImageBase.check_connected() is False:
                servers.remove(config.IMAGE_SERVER_IP)
                config.IMAGE_SERVER_IP = None
            else:
                break
        if config.IMAGE_SERVER_IP is None:
            raise EnvironmentError(f"所有IMAGE服务器不可用: {log_server}")
        self.result = ImageBase.find_element(*args, **kwargs)

        if isinstance(self.result, list):
            self.x, self.y = self.result

        return self
