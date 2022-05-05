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
    # ctrl + enter 发送消息
    gui.hotkey('ctrlleft', 'enter')
    if save_log:
        cor = conn.cursor()
        cor.execute("insert into 消息发送日志(接收人,消息) values(%s,%s)", (to_who, msg))
        conn.commit()


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
