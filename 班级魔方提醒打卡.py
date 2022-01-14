import json
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup

id_to_name = eval(open("id_to_name.txt", encoding="utf-8").read())
id_to_status = {10: "出勤",
                4: "请假",
                0: "缺勤"}
id_to_class = {31980: '18软件工程1班',
               31981: '18软件工程2班',
               41684: '19计科1班',
               41685: '19计科2班',
               41686: '19软工1班',
               41687: '19软工2班',
               41688: '19计科日双'}
class_to_qun = {'18软件工程1班': '18软件工程1班',
                '18软件工程2班': '18软件工程2班',
                '19计科1班': '19计科1通知群',
                '19计科2班': '19计科2班',
                '19计科日双': '19计科日双班',
                '19软工1班': '没有老师的软工1',
                '19软工2班': '19级软工2班'}


def n(name_id):
    return id_to_name[name_id]


def s(status_id):
    return id_to_status[status_id]


def c(class_id):
    return id_to_class[class_id]


def q(class_name):
    return class_to_qun[class_name]


import win32gui
import win32con
import win32clipboard as w
import time
import requests
import json
import os
from datetime import datetime
import pymysql
import traceback
import sys

'''update 消息发送日志 SET 人数 = length(消息)-length(REPLACE(消息, '、', '  ')) +1 WHERE 消息 != "请大家进行晚考勤打卡"'''


def getText():
    """获取剪贴板文本"""
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_UNICODETEXT)
    w.CloseClipboard()
    return d


def setText(aString):
    """设置剪贴板文本"""
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()


def send_qq(to_who, msg):
    print("sendto:%s,%s" % (to_who, msg))
    """发送qq消息
    to_who：qq消息接收人
    msg：需要发送的消息
    """
    # 将消息写到剪贴板
    setText(msg)
    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None, to_who)
    # 投递剪贴板消息到QQ窗体
    win32gui.SendMessage(qq, 258, 22, 2080193)
    win32gui.SendMessage(qq, 770, 0, 0)
    time.sleep(0.8)
    # 模拟按下回车键
    win32gui.SendMessage(qq, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.SendMessage(qq, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    cor = conn.cursor()
    cor.execute("insert into 消息发送日志(接收人,消息) values(%s,%s)", (to_who, msg))
    conn.commit()


conn = pymysql.connect(
    # host="19jike2.xyz",
    host="localhost",
    user="daka",
    password="dakadakas",
    database="小one易健康打卡",
    charset="utf8")
sess = requests.session()
sess.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Refer': 'http://www.banjimofang.com/teacher/course/13709/punch/result/397231/recent',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cookie': 'remember_teacher_59ba36addc2b2f9401580f014c7f58ea4e30989d=36678%7CJK3fy2BryAB0DRWjjGHcMpE7ooT72ZbyEw3QKdC060oCUK1bEUCcmpeIcC2t%7C%242y%2410%24W9oOJsrCW1VX7%2FSXO5Nk9.e6TXnBpP0YxDE%2FomCdHbW%2FAIHWuZzDC; yxktmf=c78o6TdA5lu9khH2Jt4JnDqf6DCdutsNeBDM1HqN'})


def get_cur_punch_url(sess):
    res = sess.get("http://www.banjimofang.com/teacher/course/13709/punch/")
    soup = BeautifulSoup(res.text, features='lxml')
    cur_punch = soup.select_one('a.weui-cell_access')
    if cur_punch:
        punch_url = 'http://www.banjimofang.com' + cur_punch['href'] + '?op=get'
        print(punch_url)
        return punch_url


def get_unpunched_students(sess, url):
    res = sess.get(url)
    data = json.loads(res.text)['data']
    return data


punch_url = get_cur_punch_url(sess)
if punch_url:
    print('当前有打卡')
data = get_unpunched_students(sess, punch_url)
class_unreport_list = {'18软件工程1班': [],
                       '18软件工程2班': [],
                       '19计科1班': [],
                       '19计科2班': [],
                       '19软工1班': [],
                       '19软工2班': [],
                       '19计科日双': []}
for i in data['0']:
    class_unreport_list[c(i['group_id'])].append(n(i['id']))
for i in class_unreport_list:
    if len(class_unreport_list[i]) > 0:
        tixing = "请"
        tixing += "、".join(class_unreport_list[i]) + "尽快完成晚考勤打卡"
        qun_name = q(i)
        print(i, tixing)
        send_qq(qun_name, tixing)
