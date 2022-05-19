import unittest

import db
from message import send_private_msg, send_group_msg
import one
from db import Clas, Counselor, Finish


class DBTest(unittest.TestCase):

    def test1(self):
        # 查询班级下对应的成员
        class_list = db.session.query(Clas).all()
        # 查询所有辅导员
        counselor_list = db.session.query(Counselor).all()
        return

    def test2(self):
        # 查询今天打卡没有完成的班级
        from sqlalchemy import func
        from datetime import datetime
        # unfinished = db.session.query(Clas, Finish) \
        #     .outerjoin(Finish) \
        #     .filter(func.to_days(Finish.time) == func.to_days(datetime.now())) \
        #     .all()
        unfinished = db.session.query(Clas) \
            .filter(Clas.class_id.not_in(db.session.query(Finish.class_id)
                                         .filter(func.to_days(Finish.time) == func.to_days(datetime.now()))
                                         .subquery())
                    ).all()
        print(unfinished)


class ServiceTest(unittest.TestCase):

    def test1(self):
        print(one.service.get_class_to_prompt())

    def test2(self):
        print(one.service.get_student_info())

    def test3(self):
        one.service.log(receiver='测试', message='测试消息')


class RequestTest(unittest.TestCase):

    def test1(self):
        for clas in one.service.get_class_to_prompt():
            print('*' * 30)
            print(clas.class_name)
            un_reported = one.request.get_unreported(clas)
            print(un_reported)

    def test2(self):
        from exceptions import TokenExpire
        for clas in one.service.get_class_list():
            try:
                print('*' * 30)
                print(clas.class_name)
                un_reported = one.request.get_unreported(clas)
                student_list = one.service.convert_one_records_to_students(un_reported)
                print(student_list)
            except TokenExpire as e:
                print(e)

    def test3(self):
        print(one.service.get_finished_class_list())


class MessageTest(unittest.TestCase):

    def test1(self):
        send_private_msg('1596953204', message='来自python')

    def test2(self):
        send_group_msg('569525430', '[CQ:at,qq=1596953204]')


class CubeAlertTest(unittest.TestCase):

    def test1(self):
        import cube
        cube.alert_class(debug=False)


class MessageClassTest(unittest.TestCase):

    def test1(self):
        # 测试私聊消息接收
        from message_type import PrivateMessage
        msg = {'font': 0, 'message': 'hi', 'message_id': -1714586584, 'message_type': 'private',
               'post_type': 'message',
               'raw_message': 'hi', 'self_id': 481409014,
               'sender': {'age': 0, 'nickname': 'null', 'sex': 'unknown', 'user_id': 1596953204},
               'sub_type': 'friend', 'target_id': 481409014, 'time': 1652066601, 'user_id': 1596953204}
        pmessage = PrivateMessage(msg=msg)
        print(pmessage)
