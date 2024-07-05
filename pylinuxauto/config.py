import enum
import os
import pathlib
import platform
import sys
import tempfile
from os import popen


@enum.unique
class DisplayServer(enum.Enum):
    wayland = "wayland"
    x11 = "x11"


@enum.unique
class PlatForm(enum.Enum):
    win = "Windows"
    linux = "Linux"
    macos = "Darwin"


class _Config:
    """配置模块"""

    PYLINUXAUTO_HOME = pathlib.Path(__file__).parent

    PASSWORD = "1"

    # IMAGE
    IMAGE_SERVER_IP = "127.0.0.1"

    IMAGE_PORT = 8889
    IMAGE_NETWORK_RETRY = 1
    IMAGE_PAUSE = 1
    IMAGE_TIMEOUT = 5
    IMAGE_MAX_MATCH_NUMBER = 100
    PIC_PATH = ""
    IMAGE_RATE = 0.9

    # OCR
    OCR_SERVER_IP = "127.0.0.1"
    OCR_PORT = 8890
    OCR_NETWORK_RETRY = 1
    OCR_PAUSE = 1
    OCR_TIMEOUT = 5
    OCR_MAX_MATCH_NUMBER = 100

    IS_LINUX = False
    IS_WINDOWS = False
    IS_MACOS = False

    # Win default path——C:\\Users\\xxxx\\AppData\\Local\\Temp
    # Linux_MacOS default path——/tmp/screen.png
    SCREEN_CACHE = os.path.join(tempfile.gettempdir(), 'screen.png')
    TMPDIR = os.path.join(tempfile.gettempdir(), 'tmpdir')

    # 显示服务器
    if os.path.exists(os.path.expanduser("~/.xsession-errors")):
        DISPLAY_SERVER = (
            os.popen("cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1")
            .read()
            .split("=")[-1]
            .strip("\n")
        )
    else:
        DISPLAY_SERVER = "x11" if os.popen("ps -ef | grep -v grep | grep kwin_x11").read() else "wayland"

    IS_X11 = DISPLAY_SERVER == DisplayServer.x11.value
    IS_WAYLAND = DISPLAY_SERVER == DisplayServer.wayland.value

    IS_IN_VIRTUALENV = sys.prefix != sys.base_prefix


config = _Config()


def wayland_environ():
    os.environ["QT_WAYLAND_SHELL_INTEGRATION"] = "kwayland-shell"
    os.environ["XDG_SESSION_DESKTOP"] = "Wayland"
    os.environ["XDG_SESSION_TYPE"] = "wayland"
    os.environ["WAYLAND_DISPLAY"] = "wayland-0"
    os.environ["GDMSESSION"] = "Wayland"
    os.environ["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"