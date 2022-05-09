#!/usr/bin/python3
import requests
import time
from tqdm import tqdm
import db
from db import AutoPunch
from exceptions import exception_handler


def check(punch: AutoPunch):
    """
    打卡操作
    :param punch
    :return:
    """
    sess = requests.session()
    sess.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) "
                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                  "Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 "
                                  "MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN "
                                  "MicroMessenger/6.6.1.1220(0x26060135) NetType/4G Language/zh_CN miniProgram",
                    "ncov-access-token": punch.auto_punch_token}
    res = sess.get("https://www.ioteams.com/ncov/api/users/last-report")
    last_report = res.json()['data']['data']
    new_report = {}
    for key in ['address', 'self_suspected', 'self_confirmed', 'family_suspected', 'family_confirmed', 'fever',
                'infected', 'description', 'at_home', 'contacted', 'passed_beijing', 'contacted_beijing']:
        new_report.update({key: last_report[key]})
    del new_report['address']['_id']
    res = sess.post("https://www.ioteams.com/ncov/api/users/dailyReport", json=new_report)
    return res.json()['msg']


@exception_handler
def auto_punch():
    """
    小one易自动打卡
    """
    # 查询所有打卡记录
    for auto_punch_record in tqdm(db.session.query(AutoPunch).filter(AutoPunch.skip == '否').all()):
        try:
            resp = check(auto_punch_record)
            print('\n%-6s' % auto_punch_record.comment, resp)
        except Exception:
            continue
    time.sleep(5)
