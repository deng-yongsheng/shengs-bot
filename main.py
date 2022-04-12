import time
import requests
import json
from datetime import datetime
import traceback
from db import get_new_connection
from message import open_all_windows, send_qq

conn = get_new_connection()


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
    if '403 Forbidden' in res.text:
        return "token失效"
    res_j = json.loads(res.text)
    unreported_num = res_j["data"]["data"]["unReportCount"]
    reported_num = res_j["data"]["data"]["reportCount"]
    print("已打卡人数：", reported_num)
    print("未打卡人数：", unreported_num)
    if int(unreported_num) > 0:
        if int(unreported_num) <= 4:
            return ("请可爱的" + "、".join(
                [item["userName"] for item in res_j["data"]["data"]["unReportUsers"]]) + "尽快完成小one易健康打卡")
        else:
            return ("请" + "、".join(
                [item["userName"] for item in res_j["data"]["data"]["unReportUsers"]]) + "尽快完成小one易健康打卡")
    else:
        return "全员打卡完毕"


if __name__ == '__main__':
    cursor = conn.cursor()
    # 打开所有的qq窗口
    open_all_windows()

    cursor.execute("""
    SELECT 班级表.id,班级表.`学院`,班级表.`班级`,班级表.`班级群名`,令牌表.token, 班级表.`联系人`
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
            item_id, dep, team, qunming, token, admin = item
            print(item)
            mess = get_unreported(token, team, dep=dep)
            if mess == "token失效":
                print(mess)
                cor = conn.cursor()
                cor.execute("insert into 错误日志(摘要,内容) values(%s,%s)", (mess, team))
                conn.commit()
                print(f"{team}token失效，请班级管理员 {admin} 重新打开小one易并登录。")
                send_qq(qunming, f"{team}token失效，请班级管理员 {admin} 重新打开小one易并登录。")
            elif mess == "全员打卡完毕":
                print(mess)
                # 打卡完成记录
                cor = conn.cursor()
                cor.execute("insert into 打卡完成记录(班级id) select id from 班级表 WHERE 班级=%s", (team))
                conn.commit()
            else:
                print(f"发送消息:{qunming}", mess)
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
