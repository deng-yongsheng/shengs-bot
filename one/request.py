from datetime import datetime
import requests

from exceptions import TokenExpire
from db import Clas, Token


def get_unreported_by_token(token: Token):
    """
    获取某个token可以查看的打卡清空
    :param token:
    :return:
    """
    sess = requests.session()
    sess.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/86.0.4240.111 Safari/537.36',
                    'ncov-access-token': token.token,
                    'Connection': 'close'
                    }
    # 获取未登录人员
    request_parameter = {'date': '%s' % (datetime.now().strftime("%Y-%m-%d")),
                         'sort': 'jobNumber',
                         'offset': '0',
                         'limit': '100'}
    with sess.get('https://www.ioteams.com/ncov/api/users/unReport/department', params=request_parameter) as res:
        if '403 Forbidden' in res.text:
            raise TokenExpire()
        else:
            res_j = res.json()
            return res_j['data']['data']['unReportUsers']


def get_unreported(clas: Clas):
    """
    获取所有未打卡的学生学号
    :param clas:
    :return:
    """
    print('%s小one易健康打卡情况' % clas.class_name)
    print(datetime.now().strftime('%Y-%m-%d, %H:%M:%S'))
    sess = requests.session()
    sess.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/86.0.4240.111 Safari/537.36',
                    'ncov-access-token': clas.token.token,
                    'Connection': 'close'
                    }
    # 获取未登录人员
    request_parameter = {'department': clas.dept.dept_name,
                         'team': clas.class_name,
                         'date': '%s' % (datetime.now().strftime("%Y-%m-%d")),
                         'sort': 'jobNumber',
                         'offset': '0',
                         'limit': '100'}
    with sess.get('https://www.ioteams.com/ncov/api/users/unReport/department', params=request_parameter) as res:
        if '403 Forbidden' in res.text:
            raise TokenExpire()
        else:
            res_j = res.json()
            return res_j['data']['data']['unReportUsers']
