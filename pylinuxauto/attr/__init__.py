#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

from funnylog2 import logger
from pylinuxauto import exceptions

from pylinuxauto.attr.depends import install_depends

install_depends()

from pylinuxauto.attr.dogtail.tree import SearchError
from pylinuxauto.attr.dogtail.tree import root
from pylinuxauto.attr.dogtail.config import config
from pylinuxauto.attr.dogtail.tree import Node
from pylinuxauto.exceptions import ElementNotFound


class Attr():
    __author__ = "mikigo<huangmingqiang@uniontech.com>"

    def __init__(self, appname=None):
        config.childrenLimit = 10000
        config.logDebugToFile = False
        config.searchCutoffCount = 2
        config.logDebugToStdOut = False
        self.appname = appname
        if appname:
            self.obj = root.application(appname)
        else:
            self.obj = root

    def __find_child(self, obj, *args, **kwargs):
        try:
            return obj.child(*args, **kwargs, retry=False)
        except SearchError:
            raise ElementNotFound(*args, **kwargs)

    def find_element_by_attr_name(
            self,
            *,
            appname: str = "",
            name: str = "",
            role_name: str = "",
            description: str = "",
            label: str = "",
            recursive: bool = True,
            retry: bool = False,
            debugName: str = None,
            showingOnly=None
    ) -> Node:
        logger.debug(f"获取元素对象【{name}】")
        if appname:
            self.obj = root.application(appname)
        element = self.__find_child(
            self.obj,
            name,
            roleName=role_name,
            description=description,
            label=label,
            recursive=recursive,
            retry=retry,
            debugName=debugName,
            showingOnly=showingOnly
        )
        logger.debug(f"获取到元素对象【{name}】:{element}")
        return element

    def find_element_by_attr_path(self, attr_path: str):
        if not attr_path.startswith("/"):
            raise ValueError
        elements = [i for i in attr_path.split("/") if i]
        if not elements:
            raise ValueError
        try:
            _obj = root.application(elements[0], retry=False)
        except SearchError:
            raise exceptions.ApplicationStartError(elements[0])
        for ele in elements[1:]:
            _obj = self.__find_child(_obj, ele)
        return _obj

    def find_elements_to_the_end(self, ele_name):
        """
         递归查找应用界面的元素(适用于查找多个同名称元素)
        :param ele_name: 需要查找的元素名称
        :return: 查找到的元素对象的列表
        """
        eles = []
        root_ele = self.obj

        def recur_inter(node=None):
            if not node:
                node = root_ele
            children = node.children
            if children:
                for i in children:
                    if i.combovalue == ele_name:
                        eles.append(i)
                    recur_inter(i)

        recur_inter()
        return eles

if __name__ == '__main__':
    dog = Attr().find_element_by_attr_name(appname="dde-dock", name="Btn_文件管理器").click()
