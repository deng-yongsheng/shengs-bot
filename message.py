import win32gui
import win32con
import time
import pyautogui as gui
import pyperclip as p

from db import get_new_connection

conn = get_new_connection()


def set_text_to_clip(string):
    """设置剪贴板文本"""
    p.copy(string)


def send_qq(to_who, msg, save_log=True):
    """
    发送qq消息
    to_who：qq消息接收人
    msg：需要发送的消息
    """
    global conn
    print("sendto:%s,%s" % (to_who, msg))
    # 将消息写到剪贴板
    set_text_to_clip(msg)
    # 获取qq群窗口句柄
    qq_group = gui.getWindowsWithTitle(to_who)[0]
    qq_group.activate()
    # 投递剪贴板消息到QQ窗体
    gui.hotkey('ctrlleft', 'v')
    time.sleep(0.8)
    # alt+enter 发送消息
    gui.hotkey('altright', 'enter')
    if save_log:
        cor = conn.cursor()
        cor.execute("insert into 消息发送日志(接收人,消息) values(%s,%s)", (to_who, msg))
        conn.commit()


def open_all_windows():
    """
    打开所有的qq群对话框
    :return:
    """
    global conn
    cursor = conn.cursor()
    cursor.execute("SELECT 班级群名,班群群号 FROM 班级表 where 班级群名 is not null and 班群群号 is not null and 不提醒='No'")
    opened_window_list = gui.getAllTitles()
    qqh = gui.getWindowsWithTitle("QQ")[0]
    for group_name, group_number in cursor.fetchall():
        if group_name not in opened_window_list:
            print("打开窗口", group_name, group_number)
            qqh.activate()
            time.sleep(1)
            gui.press("backspace")
            gui.typewrite(group_number)
            time.sleep(2)
            gui.press("enter")
            time.sleep(2)
