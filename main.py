import win32gui
import win32con
import time
import requests
import json
from datetime import datetime
import pymysql
import traceback
import pyautogui as gui
import pyperclip as p

conn = pymysql.connect(
    host="dengyongsheng.cn",
    user="daka",
    password="dakadakas",
    database="小one易健康打卡",
    charset="utf8")
cursor = conn.cursor()
cursor.execute("SELECT 班级群名,班群群号 FROM 班级表 where 班级群名 is not null and 班群群号 is not null and 不提醒='No'")
qunlist = dict(cursor.fetchall())
nowlist = gui.getAllTitles()
qqh = gui.getWindowsWithTitle("QQ")[0]
# qunlist.update({"自动打卡机器人官方群":"935513061"})
print(qunlist)
for i in qunlist:
    if (i not in nowlist):
        print("打开窗口", i, qunlist[i])
        # p.copy(qunlist[i])
        qqh.activate()
        gui.press("backspace")
        gui.typewrite(qunlist[i])
        time.sleep(2)
        gui.press("enter")


def setText(aString):
    """设置剪贴板文本"""
    p.copy(aString)


def send_qq(to_who, msg):
    print("sendto:%s,%s" % (to_who, msg))
    """发送qq消息
    to_who：qq消息接收人
    msg：需要发送的消息
    """
    # 将消息写到剪贴板
    setText(msg)
    # 获取qq窗口句柄
    qq = win32gui.FindWindow(None,
                             to_who)
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


def get_unreported(token, team, dep="计算机学院"):
    date_time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    print("%s小one易健康打卡情况" % team)
    print(date_time)
    print()
    sess = requests.session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "ncov-access-token": "%s" % token}
    sess.headers = headers
    # 获取未登录人员
    questpatameter = {'department': '%s' % dep,
                      'team': team,
                      'date': '%s' % (time.strftime("%Y-%m-%d")),
                      'sort': 'jobNumber',
                      'offset': '0',
                      'limit': '100'}
    res = sess.get("https://www.ioteams.com/ncov/api/users/unReport/department", params=questpatameter)
    # print(res.text)
    if ('403 Forbidden' in res.text):
        return "token失效"
    resj = json.loads(res.text)
    unreport_num = resj["data"]["data"]["unReportCount"]
    reported_num = resj["data"]["data"]["reportCount"]
    print("已打卡人数：", reported_num)
    print("未打卡人数：", unreport_num)
    if (int(unreport_num) > 0):
        if (int(unreport_num) <= 4):
            return ("请可爱的" + "、".join(
                [item["userName"] for item in resj["data"]["data"]["unReportUsers"]]) + "尽快完成小one易健康打卡")
        else:
            return ("请" + "、".join(
                [item["userName"] for item in resj["data"]["data"]["unReportUsers"]]) + "尽快完成小one易健康打卡")
    else:
        return "全员打卡完毕"


conn.commit()
cursor.execute("""
SELECT 班级表.id,班级表.`学院`,班级表.`班级`,班级表.`班级群名`,令牌表.token 
FROM 令牌表,班级表
WHERE 令牌表.`班级id`= 班级表.id 
    and `班级表`.`不提醒` = 'No'
    and 令牌表.id IN 
        (SELECT MAX(id) FROM 令牌表
        GROUP BY 班级id) 
    and 班级表.id NOT IN
        (select 班级id from 打卡完成记录 where 完成时间 IN 
        (select max(完成时间) FROM 打卡完成记录 
        WHERE to_days(NOW()) = TO_DAYS(完成时间) group by 班级id))
order by 班级表.id
""")
for item in cursor.fetchall():
    print("*" * 40)
    try:
        item_id, dep, team, qunming, token = item
        print(item)
        # qunming = "自动化测试"
        mess = get_unreported(token, team, dep=dep)
        # mess = "测试"
        if (mess == "token失效"):
            print(mess)
            cor = conn.cursor()
            cor.execute("insert into 错误日志(摘要,内容) values(%s,%s)", (mess, team))
            conn.commit()
            send_qq(qunming, team + "token失效" + "，请班级管理员联系邓永盛。")
        elif (mess == "全员打卡完毕"):
            print(mess)
            # 打卡完成记录
            cor = conn.cursor()
            cor.execute("insert into 打卡完成记录(班级id) select id from 班级表 WHERE 班级=%s", (team))
            conn.commit()
        else:
            print("发送消息:", mess)
            send_qq(qunming, mess)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        cor = conn.cursor()
        cor.execute("insert into 错误日志(摘要,内容) values(%s,%s)", (str(e), traceback.format_exc()))
        conn.commit()
        continue

# 今天已经完成打卡的班级
cursor.execute("""
SELECT 班级表.id,班级表.`班级`,班级表.`班级群名`,令牌表.token 
FROM 令牌表,班级表
WHERE 令牌表.`班级id`= 班级表.id 
    and 不提醒='No'
    and 令牌表.id IN 
        (SELECT MAX(id) FROM 令牌表
        GROUP BY 班级id) 
    and 班级表.id IN
        (select 班级id from 打卡完成记录 where 完成时间 IN 
        (select max(完成时间) FROM 打卡完成记录 
        WHERE to_days(NOW()) = TO_DAYS(完成时间) group by 班级id))
""")
print("以下班级已经完成打卡，今天不再发送消息提醒：")
for item in cursor.fetchall():
    item_id, team, qunming, token = item
    print("\t" + team)

time.sleep(5)
