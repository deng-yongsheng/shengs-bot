import unittest

import db
from message import send_private_msg, send_group_msg
from scripts import one
import request
import service
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
        print(service.get_class_to_prompt())

    def test2(self):
        print(service.get_student_info())

    def test3(self):
        service.log(receiver='测试', message='测试消息')


class RequestTest(unittest.TestCase):

    def test1(self):
        for clas in service.get_class_to_prompt():
            print('*' * 30)
            print(clas.class_name)
            un_reported = request.one.get_unreported(clas)
            print(un_reported)

    def test2(self):
        for clas in service.get_class_list():
            print('*' * 30)
            print(clas.class_name)
            un_reported = request.one.get_unreported(clas)
            student_list = service.convert_numbers_to_students(un_reported)
            print(student_list)

    def test3(self):
        print(service.get_finished_class_list())


class MessageTest(unittest.TestCase):

    def test1(self):
        send_private_msg('1596953204', message='来自python')

    def test2(self):
        send_group_msg('569525430', '[CQ:at,qq=1596953204]')


class AlertTest(unittest.TestCase):

    def test1(self):
        one.alert_classes(debug=True)
