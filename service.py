import unittest
from typing import List

from sqlalchemy import func
from datetime import datetime
import db
from model import Finish, Student, Clas, Log

student_info = None


def get_class_to_prompt() -> list:
    """
    获取没有完成打卡的班级列表
    :return:
    """
    return db.session.query(Clas) \
        .filter(Clas.class_id.not_in(db.session.query(Finish.class_id)
                                     .filter(func.to_days(Finish.time) == func.to_days(datetime.now()))
                                     .subquery())
                ).all()


def get_class_list() -> List[Clas]:
    """
    获取班级列表
    :return:
    """
    return db.session.query(Clas).all()


def get_student_info():
    """
    获取学生信息列表
    :return:
    """
    global student_info
    if student_info is None:
        student_info = db.session.query(Student).all()
    return student_info


def log(receiver: str, message: str):
    """
    记录消息发送日志
    :param receiver: 消息接收人
    :param message: 消息内容
    :return:
    """
    with db.session.begin():
        log_record = Log(receiver=receiver, message=message)
        db.session.add(log_record)


def class_finished(class_: Clas):
    """
    某个班级完成了打卡，不再进行提醒
    :param class_:
    :return:
    """
    with db.session.begin():
        finish_record = Finish(class_id=class_.class_id)
        db.session.add(finish_record)


class Test(unittest.TestCase):

    def test1(self):
        print(get_class_to_prompt())

    def test2(self):
        print(get_student_info())

    def test3(self):
        log(receiver='测试', message='测试消息')
