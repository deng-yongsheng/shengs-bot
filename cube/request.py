import json
import re
import requests
from bs4 import BeautifulSoup

from cube import service
from db import CubeAutoPunch
from exceptions import StudentNotInDatabase


def generate_session() -> requests.Session:
    i_sess = requests.session()
    i_sess.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.63 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Refer': 'http://www.banjimofang.com/teacher/course/13709/punch/result/397231/recent',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cookie': 'remember_teacher_59ba36addc2b2f9401580f014c7f58ea4e30989d=36678%7CJK3fy2BryAB0DRWjjGHc'
                  'MpE7ooT72ZbyEw3QKdC060oCUK1bEUCcmpeIcC2t%7C%242y%2410%24W9oOJsrCW1VX7%2FSXO5Nk9.e6TXnB'
                  'pP0YxDE%2FomCdHbW%2FAIHWuZzDC; yxktmf=c78o6TdA5lu9khH2Jt4JnDqf6DCdutsNeBDM1HqN'})
    return i_sess


sess = generate_session()


def get_cur_punch_url_list() -> list:
    """
    获取当前的所有打卡链接
    :return:
    """
    res = sess.get('https://k8n.cn/teacher/course/13709/punch/')
    soup = BeautifulSoup(res.text, features='lxml')
    punch_list = ['https://k8n.cn' + cur_punch['href'] for cur_punch in
                  soup.select('a.weui-cell_access')]
    return punch_list


def get_leave(url: str) -> set:
    """
    获取请假且离校人员名单
    :param url:
    :return:
    """
    res = sess.get(url)
    json_str_res = re.search(r'(?<=leaving_students = )\[.*\](?=;)', res.text)
    if json_str_res:
        json_str = json_str_res.group()
        j = json.loads(json_str)
        ask_and_leave_school = [i['student_id'] for i in j if i['leave_school'] == 1]
        return set(ask_and_leave_school)
    else:
        return set()


def get_student_info_list() -> dict:
    """
    从小one易获取学生信息列表
    :return:
    """
    res = sess.get('https://www.banjimofang.com/teacher/course/13709/data/students')
    return res.json()


def get_unpunched_students(punch_url) -> dict:
    """
    获取班级没有打卡学生名单
    :param punch_url:
    :return:
    """
    res = sess.get(punch_url + '?op=get')
    res_j = res.json()

    if 'data' in res_j:
        res_j = res_j['data']
    # 获取所有的没有完成打卡人员的班级信息
    class_cube_id_list = set(map(lambda x: x['group_id'], res_j.get('0')))
    unfinished_class = dict([(cube_id, service.query_class_by_cube_id(cube_id)) for cube_id in class_cube_id_list])
    group_by_class = dict.fromkeys(unfinished_class.values())
    for key in group_by_class:
        group_by_class[key] = []
    # 获取已经请假离校了的学生
    ask_and_leave_list = get_leave(punch_url)
    # 将所有未完成打卡的学生归到班级
    for record in res_j.get('0'):
        if record['id'] not in ask_and_leave_list:
            student = service.query_student_by_cube_id(record['id'])
            if student is None:
                # 如果查不到记录则报错
                raise StudentNotInDatabase(str(record))
            group_by_class[unfinished_class[record['group_id']]].append(student)
    return group_by_class


def set_punch_state(t_punch_url, punch_record: CubeAutoPunch):
    """
    修改打卡状态
    :param t_punch_url: 打卡的链接
    :param punch_record: 自动打卡记录
    :return:
    """
    sess.get(t_punch_url + f'?op=set&sid={punch_record.student.cube_id}&status={punch_record.cube_punch_state_id}')
    print(f'将{punch_record.student.student_name} 的打卡状态修改为 {punch_record.cube_punch_state.cube_punch_state_name}')
