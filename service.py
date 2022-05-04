import unittest
from sqlalchemy import and_, func
from datetime import datetime
import db
from model import Finish, Student, Clas, Token

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


def get_student_info():
    """
    获取学生信息列表
    :return:
    """
    global student_info
    if student_info is None:
        student_info = db.session.query(Student).all()
    return student_info


class Test(unittest.TestCase):

    def test1(self):
        print(get_class_to_prompt())

    def test2(self):
        print(get_student_info())
