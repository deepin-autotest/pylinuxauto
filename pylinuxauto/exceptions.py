
from funnylog2 import logger

class ElementNotFound(Exception):

    def __init__(self, name):
        """
        未找到元素
        :param name: 命令
        """
        err = f"未找到元素: {name}"
        logger.error(err)
        Exception.__init__(self, err)

class TemplateElementNotFound(BaseException):
    """通过模板资源未匹配到对应元素"""

    def __init__(self, *name):
        """
        通过模板资源未匹配到对应元素
        :param name: 命令
        """
        err = f"通过图片资源, 未在屏幕上匹配到元素"
        template = [f"{i}" for i in name]
        logger.error(*template)
        BaseException.__init__(self, err, *template)


class TemplatePictureNotExist(BaseException):
    """图片资源，文件不存在"""

    def __init__(self, name):
        """
        文件不存在
        :param name: 命令
        """
        err = f"图片资源文件不存在: {name}"
        logger.error(err)
        BaseException.__init__(self, err)


class ApplicationStartError(Exception):
    """
    应用程序未启动
    """

    def __init__(self, result):
        """
        应用程序未启动
        :param result: 结果
        """
        err = f"应用程序未启动: {result}"
        logger.error(err)
        Exception.__init__(self, err)


class GetWindowInformation(Exception):
    """获取窗口信息错误"""

    def __init__(self, msg):
        """
        获取窗口信息错误
        """
        logger.error(msg)
        Exception.__init__(self, msg)


class NoSetReferencePoint(Exception):
    """没有设置参考点"""

    def __init__(self, msg):
        err = f"没有设置参考点: {msg}"
        logger.error(err)
        Exception.__init__(self, err)