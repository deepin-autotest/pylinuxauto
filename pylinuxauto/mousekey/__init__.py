#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.
# SPDX-License-Identifier: GPL-2.0-only

import os
from time import sleep

from funnylog2 import logger

from pylinuxauto.mousekey import pyautogui

pyautogui.FAILSAFE = False

__author__ = "mikigo<huangmingqiang@uniontech.com>"

MOUSE = {1: pyautogui.PRIMARY, 2: pyautogui.MIDDLE, 3: pyautogui.RIGHT}


def screen_size():
    """
     获取屏幕大小
     width, height
    """
    width, height = pyautogui.size()
    logger.debug(f"获取屏幕分辨率 {width}*{height}")
    return width, height


def current_location(out_log=True):
    """
     获取当前鼠标位置
     鼠标当前的坐标
    """
    position = pyautogui.position()
    if out_log:
        logger.debug(f"当前鼠标坐标 {position}")
    return position


def move_to(_x, _y, duration=0.4):
    """
     移动到指定位置
    :param _x: x
    :param _y: y
    :param duration:移动的速度
    """
    logger.debug(f"鼠标移动至 ({_x, _y}, 速度：{duration})")
    pyautogui.moveTo(int(_x), int(_y), duration=duration)


def move_rel(_x, _y, duration=0.4):
    """
     相对移动到位置
    :param _x:
    :param _y:
    :param duration:
    """
    logger.debug(f"鼠标移动相对坐标位置 ({_x, _y}), 速度：{duration}")
    pyautogui.moveRel(xOffset=int(_x), yOffset=int(_y), duration=duration)


def click(_x=None, _y=None):
    """
     点击鼠标左键
    :param _x:
    :param _y:
    :param _type: 使用 PyAutoGUI or Xdotool 点击
    """
    logger.debug(f"点击坐标 {(_x, _y) if _x else current_location(out_log=False)}")
    pyautogui.click(x=_x, y=_y)


def move_rel_and_click(_x, _y):
    """
     move relative and click
    :param _x:
    :param _y:
    """
    move_rel(_x, _y)
    click()


def middle_click():
    """
    单击鼠标滚轮中间
    """
    logger.debug("单击鼠标滚轮中间")
    pyautogui.middleClick()


def right_click(_x=None, _y=None):
    """
     单击鼠标右键
    :param _x:
    :param _y:
    """
    logger.debug(f"鼠标右键坐标 {(_x, _y) if _x else current_location(out_log=False)}")
    pyautogui.rightClick(x=_x, y=_y)


def double_click(_x=None, _y=None, interval=0.3):
    """
     双击鼠标左键
    :param _x:
    :param _y:
    :param interval: 两次点击的间隔，默认 0.3s
    """
    logger.debug(f"鼠标左键双击坐标 {(_x, _y) if _x else current_location(out_log=False)}")
    pyautogui.doubleClick(x=_x, y=_y, interval=interval)


def triple_click(_x=None, _y=None):
    """
     三击鼠标左键
    :param _x:
    :param _y:
    """
    logger.debug(f"鼠标三连击坐标 {(_x, _y) if _x else current_location(out_log=False)}")
    pyautogui.tripleClick(x=_x, y=_y, interval=0.3)


def drag_to(_x, _y, duration=0.4, delay=1):
    """
     拖拽到指定位置(绝对位置)
    :param _x: 拖拽到的位置x
    :param _y: 拖拽到的位置y
    :param duration: 拖拽的时长
    :param delay: 拖拽后等待的时间
    """
    logger.debug(f"鼠标从当前位置拖拽到坐标 ({_x, _y})")
    pyautogui.dragTo(x=int(_x), y=int(_y), duration=duration, mouseDownUp=True)
    sleep(delay)


def drag_rel(_x, _y):
    """
     按住鼠标左键,拖拽到指定位置(相对位置)
    :param _x: 拖拽的相对位置x，正数向右，负数向左
    :param _y: 拖拽的相对位置y，正数向下，负数向上
    """
    logger.debug(f"鼠标从当前位置拖拽到相对坐标 ({_x, _y})")
    pyautogui.dragRel(xOffset=int(_x), yOffset=int(_y), duration=0.4, mouseDownUp=True)


def mouse_down(_x=None, _y=None, button=1):
    """
     按住鼠标键不放
    :param _x:
    :param _y:
    :param button: 1 左键， 2 中键， 3 右键
    """
    logger.debug(
        f"在坐标 {(_x, _y) if _x else current_location(out_log=False)} "
        f"处按住鼠标{['左', '中', '右'][button - 1]}键不放"
    )
    pyautogui.mouseDown(x=_x, y=_y, button=MOUSE.get(button, pyautogui.PRIMARY))


def mouse_up(button=1):
    """
     松开鼠标左键
    :param button: 1 左键， 2 中键， 3 右键
    """
    logger.debug(f"松开鼠标{['左', '中', '右'][button - 1]}键")
    pyautogui.mouseUp(button=MOUSE.get(button, pyautogui.PRIMARY))


def mouse_scroll(amount_of_scroll, duration=1):
    """
     滚动鼠标滚轮,the_amount_of_scroll为传入滚轮数,正数为向上,负数为向下
    :param amount_of_scroll: 滚轮数
    :param duration:
    """
    pyautogui.scroll(amount_of_scroll)
    if amount_of_scroll > 0:
        direct = "上"
    else:
        direct = "下"
    logger.debug(f"向<{direct}>滑动滚轮")
    sleep(duration)


def input_message(
        message,
        delay_time: int = 300,
        interval: [int, float] = 0.2,
):
    """
     输入字符串
    :param message: 输入的内容
    :param delay_time: 延迟时间
    :param interval:
    """
    logger.debug(f"输入字符串<{message}>")
    message = str(message)

    def check_chinese():
        for _ch in message:
            if "\u4e00" <= _ch <= "\u9fff":
                return True
        return False

    if check_chinese():
        os.system(f"xdotool type --delay {delay_time} '{message}'")
    else:
        pyautogui.typewrite(message=str(message), interval=interval)


input = input_message


def press_key(key: str, interval=0.0):
    """
     键盘上指定的按键
    :param key: 键盘按键
    :param interval:
    """
    logger.debug(f"点击键盘上指定的按键<{key}>, 间隔<{interval}>")
    pyautogui.press(key, interval=interval)


def press_key_down(key: str):
    """
     按住键盘按键不放
    :param key: 键盘按键
    """
    logger.debug(f"按下<{key}>按键")
    pyautogui.keyDown(key)


def press_key_up(key: str):
    """
     放松按键
    :param key: 键盘按键
    """
    logger.debug(f"放松<{key}>按键")
    pyautogui.keyUp(key)


def hot_key(*args, interval=0.03):
    """
     键盘组合按键操作
    :param args: 键盘组合键，比如："ctrl","alt","a"
    """
    logger.debug(f"快捷键 {args}")
    pyautogui.hotkey(*args, interval=interval)


def hot_key_down(*args):
    """
     组合按键按下不放
    :param args:
    """
    for _c in args:
        if len(_c) > 1:
            _c = _c.lower()
        press_key_down(_c)
        sleep(0.03)


def hot_key_up(*args):
    """
     组合按键释放
    :param args:
    """
    for c in reversed(args):
        if len(c) > 1:
            c = c.lower()
        press_key_up(c)
        sleep(0.03)


def move_to_and_click(_x, _y):
    """
     移动到某个位置点击
    :param _x: 移动到的位置 x
    :param _y: 移动到的位置 y
    """
    move_to(_x, _y)
    click()


def move_to_and_right_click(_x, _y):
    """
     移动到某个位置点击右键
    :param _x: 移动到的位置 x
    :param _y: 移动到的位置 y
    """
    move_to(_x, _y)
    right_click()


def move_to_and_double_click(_x, _y):
    """
     移动到某个位置点击双击
    :param _x: 移动到的位置 x
    :param _y: 移动到的位置 y
    """
    move_to(_x, _y)
    double_click()


def move_on_and_drag_to(start: tuple, end: tuple):
    """
     指定拖动的起始-终止坐标
    :param start: 开始坐标
    :param end: 终止坐标
    """
    move_to(*start)
    drag_to(*end)


def move_on_and_drag_rel(start: tuple, end: tuple):
    """
     指定拖动的起始-终止坐标
    :param start: 开始坐标
    :param end: 终止坐标
    """
    move_to(*start)

    drag_rel(*end)


def select_menu(number: int):
    """
     选择桌面右键菜单中的选项(从上到下)
    :param number: 在菜单中的位置数
    """
    logger.debug(f"选择右键菜单中的选项(从上到下)第{number}项")
    for _ in range(number):
        press_key("down")
    sleep(0.3)
    press_key("enter")


def reverse_select_menu(number: int):
    """
     选择桌面右键菜单中的选项（从下到上）
    :param number: 在菜单中的位置数
    """
    logger.debug(f"选择右键菜单中的选项(从下到上)第{number}项")
    for _ in range(number):
        press_key("up")
    sleep(0.3)
    press_key("enter")


def select_submenu(number: int):
    """
     选择右键菜单中的子菜单选项（从上到下）
    :param number: 在菜单中的位置数
    """
    for _ in range(1, number):
        press_key("down")
    press_key("enter")


def draw_line(start_x, start_y, rel_x, rel_y):
    """
     从某个坐标开始画线（框选）
    :param start_x: 开始的坐标的横坐标
    :param start_y: 开始的坐标的纵坐标
    :param rel_x: 向量的横坐标
    :param rel_y: 向量的纵坐标
    """
    move_to(start_x, start_y)
    drag_rel(rel_x, rel_y)


# ========== ctrl ==========
def ctrl_f9():
    hot_key("ctrl", "f9")


def ctrl_shift_forward_slash_down():
    hot_key_down("ctrl", "shift", "/")


def ctrl_shift_forward_slash_up():
    hot_key_up("ctrl", "shift", "/")


def ctrl_a():
    hot_key("ctrl", "a")


def ctrl_l():
    hot_key("ctrl", "l")


def ctrl_g():
    hot_key("ctrl", "g")


def ctrl_n():
    hot_key("ctrl", "n")


def ctrl_alt_t():
    hot_key("ctrl", "alt", "t")


def ctrl_alt_down():
    hot_key("ctrl", "alt", "down")


def ctrl_alt_up():
    hot_key("ctrl", "alt", "up")


def ctrl_alt_a():
    hot_key("ctrl", "alt", "a")


def ctrl_x():
    hot_key("ctrl", "x")


def ctrl_s():
    hot_key("ctrl", "s")


def ctrl_f():
    hot_key("ctrl", "f")


def ctrl_v():
    hot_key("ctrl", "v")


def ctrl_c():
    hot_key("ctrl", "c")


def ctrl_z():
    hot_key("ctrl", "z")


def ctrl_y():
    hot_key("ctrl", "y")


def ctrl_i():
    hot_key("ctrl", "i")


def ctrl_h():
    hot_key("ctrl", "h")


def ctrl_o():
    hot_key("ctrl", "o")


def ctrl_shift_up():
    hot_key("ctrl", "shift", "up")


def ctrl_shift_n():
    hot_key("ctrl", "shift", "n")


def ctrl_shift_down():
    hot_key("ctrl", "shift", "down")


def ctrl_shift_left():
    hot_key("ctrl", "shift", "left")


def ctrl_shift_right():
    hot_key("ctrl", "shift", "right")


def ctrl_up():
    hot_key("ctrl", "up")


def ctrl_down():
    hot_key("ctrl", "down")


def ctrl_left():
    hot_key("ctrl", "left")


def ctrl_right():
    hot_key("ctrl", "right")


def ctrl_rod():
    """ctrl + '-'"""
    hot_key("ctrl", "-")


def ctrl_add():
    hot_key("ctrl", "+")


def ctrl_r():
    hot_key("ctrl", "r")


def ctrl_shift_r():
    hot_key("ctrl", "shift", "r")


def ctrl_shift_z():
    hot_key("ctrl", "shift", "z")


def ctrl_scroll(direction, amount_of_scroll=1):
    """ctrl + 滚轮"""
    press_key_down("ctrl")
    for _ in range(amount_of_scroll):
        mouse_scroll(direction, duration=0)
    press_key_up("ctrl")


def ctrl_e():
    hot_key("ctrl", "e")


def ctrl_shift_s():
    hot_key("ctrl", "shift", "s")


def ctrl_shift():
    hot_key("ctrl", "shift")


def ctrl_space():
    hot_key("ctrl", "space")


def ctrl_shift_e():
    hot_key("ctrl", "shift", "e")


def ctrl_shift_w():
    hot_key("ctrl", "shift", "w")


def ctrl_alt_v():
    hot_key("ctrl", "alt", "v")


def ctrl_printscreen():
    hot_key("ctrl", "printscreen")


def ctrl_tab():
    hot_key("ctrl", "tab")


def ctrl_shift_tab():
    hot_key("ctrl", "shift", "tab")


# ========== shift ==========


def shift():
    hot_key("shift")


def shift_right():
    hot_key("shift", "right")


def shift_down():
    hot_key("shift", "down")


def shift_up():
    hot_key("shift", "up")


def shift_delete():
    hot_key("shift", "delete")


def shift_left():
    hot_key("shift", "left")


def shift_space():
    hot_key("shift", "space")


def shift_scroll(direction, amount_of_scroll=1):
    """shift + 滚轮"""
    press_key_down("shift")
    for _ in range(amount_of_scroll):
        mouse_scroll(direction, duration=0)
    press_key_up("shift")


# ========== alt ==========


def alt_tab():
    hot_key("alt", "tab")


def alt_m():
    hot_key("alt", "m")


def alt_f4():
    hot_key("alt", "f4")


def alt_f2():
    hot_key("alt", "f2")


def alt_enter():
    hot_key("alt", "enter")


def alt_o():
    hot_key("alt", "o")


def alt_s():
    hot_key("alt", "s")


def alt_p():
    hot_key("alt", "p")


def alt_d():
    hot_key("alt", "d")


def alt_shift_tab():
    hot_key("alt", "shift", "tab")


def alt_printscreen():
    hot_key("alt", "PrintScreen")


# ========== win ==========


def win_up():
    hot_key("win", "up")


def win_d():
    hot_key("win", "d")


def win():
    hot_key("win")


def win_left():
    hot_key("win", "left")


def win_right():
    hot_key("win", "Right")


def winleft_d():
    hot_key("winleft", "d")


def winleft_q():
    hot_key("winleft", "q")


def winleft_e():
    hot_key("winleft", "e")


# ========== single key ==========

def tab():
    press_key("tab")


def esc():
    press_key("esc")


def right():
    press_key("right")


def left():
    press_key("left")


def up():
    press_key("up")


def down():
    press_key("down")


def dot():
    press_key(".")


def press_left_sometime(sometime: int):
    """
    按住键盘方向键-左键一段时间
    :param sometime: 一段时间
    """
    press_key_down("left")
    sleep(sometime)
    press_key_up("left")


def press_up_sometime(sometime: int):
    """
    按住键盘方向键-上键一段时间
    :param sometime: 一段时间
    """
    press_key_down("up")
    sleep(sometime)
    press_key_up("up")


def enter():
    press_key("enter")


def f1():
    press_key("f1")


def f2():
    press_key("f2")


def f3():
    press_key("f3")


def f4():
    press_key("f4")


def f5():
    press_key("f5")


def space():
    press_key("space")


def backspace():
    press_key("backspace")


def delete():
    press_key("delete")


def printscreen():
    hot_key("printscreen")


def p():
    press_key("p")


def h():
    press_key("h")


def f():
    press_key("f")


def s():
    press_key("s")


def o():
    press_key("o")


def r():
    press_key("r")


def i():
    press_key("i")


def pageup():
    press_key("pageup")


def pagedown():
    press_key("pagedown")
