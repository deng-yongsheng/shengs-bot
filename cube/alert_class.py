from typing import List

from db import Clas, Student
from message import message
from . import request
from . import service


def alert_class(debug=False):
    """
    班级魔方考勤提醒
    :return:
    """
    # 获取打卡列表
    punch_list = request.get_cur_punch_url()
    if punch_list:
        print('当前有打卡')
        for punch_url in punch_list:
            # 读取没有打卡的学生名单
            group_by_class = request.get_unpunched_students(punch_url)
            for clas, student_list in group_by_class.items():
                clas: Clas
                student_list: List[Student]
                # 是否添加 可爱的xx
                if_cute = '可爱' if len(student_list) <= 4 else ''
                mess = '请' + if_cute + '、'.join(map(lambda x: x.student_name, student_list)) + "尽快完成班级魔方考勤打卡"
                if len(student_list) <= 20 and student_list[0].student_qq is not None:
                    mess += '\n'
                    for stu in student_list:
                        if stu.student_qq is not None:
                            mess += f'[CQ:at,qq={stu.student_qq}]'
                print(clas.class_name)
                print(mess.replace('\n', ''))
                # 发送消息
                if not debug:
                    message.send_group_msg(clas.class_group_number, mess)
    else:
        print('当前无打卡，退出程序')


def update_student_info():
    """
    更新学生信息
    """
    pass
