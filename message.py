import win32gui
import win32con
import time
import pyautogui as gui
import pyperclip as p

import service


def set_text_to_clip(msg_to_clip):
    """
    设置剪贴板文本
    :param msg_to_clip:
    :return:
    """
    p.copy(msg_to_clip)


def send_qq_with_at(to_who, msg, save_log=True):
    """
    发送qq群消息，并自动@
    :param to_who:
    :param msg:
    :param save_log:
    :return:
    """
    print("sendto:%s,%s" % (to_who, msg))
    # 将消息写到剪贴板
    set_text_to_clip(msg)
    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None, to_who)
    # 投递剪贴板消息到QQ窗体
    win32gui.SendMessage(qq, 258, 22, 2080193)
    win32gui.SendMessage(qq, 770, 0, 0)
    time.sleep(0.8)
    # 模拟按下回车键
    win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    if save_log:
        # 发送消息记入日志
        service.log(receiver=to_who, message=msg)


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
            gui.typewrite(clas.class_group_number, interval=0.25)
            time.sleep(2)
            gui.press("enter")
            time.sleep(2)
