import os


def _screenshot_cmd():
    return "dbus-send --session --print-reply=literal --dest=org.kde.KWin /Screenshot org.kde.kwin.Screenshot"


def screenshot_full():
    return os.popen(f"{_screenshot_cmd()}.screenshotFullscreen").read().strip().strip("\n")


def screenshot_area(x, y, w, h):
    return (
        os.popen(f"{_screenshot_cmd()}.screenshotArea int32:{x} int32:{y} int32:{w} int32:{h}")
        .read()
        .strip()
        .strip("\n")
    )
