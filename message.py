import time
from typing import List
import pyperclip
import pyautogui

import service
from models import Student


def set_text_to_clip(msg_to_clip):
    """
    设置剪贴板文本
    :param msg_to_clip:
    :return:
    """
    pyperclip.copy(msg_to_clip)


def at_group_members(at_list: List[Student] = None):
    """
    @群成员
    :param at_list:
    :return:
    """
    if at_list:
        for stu in at_list:
            if stu.student_qq:
                pyautogui.write('@' + str(stu.student_qq))
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(0.3)
        # 最后一个@完后，按下空格键
        pyautogui.typewrite(' ')
        time.sleep(0.25)


def send_qq_with_at(to_who, msg, at_list: List[Student] = None):
    """
    发送qq消息，支持@功能
    :param to_who：qq消息接收人
    :param msg：需要发送的消息
    :param at_list: 需要@的成员列表
    :return:
    """
    print(f'sendto: {to_who}   msg:{msg}')
    # 将消息写到剪贴板
    set_text_to_clip(msg)
    # 获取qq群窗口句柄
    qq_group = pyautogui.getWindowsWithTitle(to_who)[0]
    qq_group.activate()
    # 投递剪贴板消息到QQ窗体
    pyautogui.hotkey('ctrlleft', 'v')
    time.sleep(0.8)
    # @成员，每次最多@20个成员
    # 先@前 20 个
    if at_list is not None and len(at_list) <= 20:
        # 少于20人时再进行@
        at_group_members(at_list)
    time.sleep(0.5)
    # 发送消息
    pyautogui.hotkey('alt', 's')
    # 再尝试发送一次
    time.sleep(1)
    pyautogui.hotkey('alt', 's')
    time.sleep(2)
    # 记入日志
    service.log(to_who, msg)


def open_all_windows():
    """
    打开所有的qq群对话框
    :return:
    """
    # 获取已经打开的窗口列表
    opened_window_list = pyautogui.getAllTitles()
    # 获取QQ主窗体的句柄
    qqh = pyautogui.getWindowsWithTitle("QQ")[0]
    # 遍历班级列表
    for clas in service.get_class_list():
        # 检查没有打开的窗口
        if clas.class_group_name not in opened_window_list:
            print("打开窗口", clas.class_group_name, clas.class_group_number)
            qqh.activate()
            time.sleep(1)
            pyautogui.press("backspace")
            pyautogui.write(clas.class_group_number, interval=0.25)
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(2)
