import unittest

import request
import service
import exceptions
from message import send_qq_with_at
import request


def alert_classes():
    """
    班级魔方考勤提醒
    :return:
    """
    # 获取打卡列表
    punch_list = request.cube.get_cur_punch_url()
    punch_list = [
        'http://www.banjimofang.com/teacher/course/13709/punch/result/791738/recent'
    ]
    if punch_list:
        print('当前有打卡')
        for punch_url in punch_list:
            # 获取请假学生名单
            qingjia_list = punch_url
            # 读取没有打卡的学生名单
            data = request.cube.get_unpunched_students(punch_url)
            # class_unreport_list = {'18软件工程1班': [],
            #                        '18软件工程2班': [],
            #                        '19计科1班': [],
            #                        '19计科2班': [],
            #                        '19软工1班': [],
            #                        '19软工2班': [],
            #                        '19计科日双': []}
            for clas in service.get_cube_classes():
                for stu_cube_id in data['0']:
                    # 判断不在请假离校名单里
                    if stu_cube_id['id'] not in qingjia_list:
                        class_unreport_list[id_to_class(stu_cube_id['group_id'])].append(id_to_name(stu_cube_id['id']))

                for i in class_unreport_list:
                    if '朱昊' in class_unreport_list[i]:
                        class_unreport_list[i].remove('朱昊')
                    if len(class_unreport_list[i]) > 0:
                        tixing = '请' + '、'.join(class_unreport_list[i]) + '尽快完成晚考勤打卡'
                        qun_name = class_to_qun_name(i)
                        print(i, tixing)
                        # send_qq(qun_name, tixing)


    else:
        print('当前无打卡，退出程序')


class Test(unittest.TestCase):

    def test1(self):
        alert_classes()
