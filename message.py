import math
import time
from typing import List
import pyautogui as gui
import pyperclip as p

import service
from models import Student


def set_text_to_clip(msg_to_clip):
    """
    设置剪贴板文本
    :param msg_to_clip:
    :return:
    """
    p.copy(msg_to_clip)


def send_qq_with_at(to_who, msg, at_list: List[Student] = None):
    """
    发送qq消息，支持@功能
    :param to_who：qq消息接收人
    :param msg：需要发送的消息
    :param at_list: 需要@的成员列表
    :return:
    """
    # 将消息写到剪贴板
    set_text_to_clip(msg)
    # 获取qq群窗口句柄
    qq_group = gui.getWindowsWithTitle(to_who)[0]
    qq_group.activate()
    # 投递剪贴板消息到QQ窗体
    gui.hotkey('ctrlleft', 'v')
    time.sleep(0.8)
    # @成员，每次最多@20个成员
    # 先@前 20 个
    if at_list is not None:
        for stu in at_list[:20]:
            if stu.student_qq:
                gui.write('@' + str(stu.student_qq))
    # ctrl + enter 发送消息
    gui.hotkey('ctrlleft', 'enter')
    # 记入日志
    service.log(to_who, msg)
    # @剩余成员
    if at_list is not None and len(at_list) > 20:
        for split_start in range(1, math.ceil(len(at_list) / 20)):
            for stu in at_list[split_start:split_start + 20]:
                if stu.student_qq:
                    gui.write('@' + str(stu.student_qq))
            # 发送消息
            gui.hotkey('ctrlleft', 'enter')


def open_all_windows():
    """
    打开所有的qq群对话框
    :return:
    """
    # 获取已经打开的窗口列表
    opened_window_list = gui.getAllTitles()
    # 获取QQ主窗体的句柄
    qqh = gui.getWindowsWithTitle("QQ")[0]
    # 遍历班级列表
    for clas in service.get_class_list():
        # 检查没有打开的窗口
        if clas.class_group_name not in opened_window_list:
            print("打开窗口", clas.class_group_name, clas.class_group_number)
            qqh.activate()
            time.sleep(1)
            gui.press("backspace")
            gui.write(clas.class_group_number, interval=0.25)
            time.sleep(2)
            gui.press("enter")
            time.sleep(2)
