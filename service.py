from typing import List

from sqlalchemy import func
from datetime import datetime
import db
from db import Finish, Student, Clas, Log

student_info = None
student_map = None


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


def get_student_info() -> List[Student]:
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
    # with db.session.begin():
    log_record = Log(receiver=receiver, message=message)
    db.session.add(log_record)
    db.session.commit()


def class_finished(class_: Clas):
    """
    某个班级完成了打卡，不再进行提醒
    :param class_:
    :return:
    """
    # with db.session.begin():
    finish_record = Finish(class_id=class_.class_id)
    db.session.add(finish_record)
    db.session.commit()


def get_finished_class_list() -> List[Clas]:
    """
    获取今天已经打卡完成了的班级
    :return:
    """
    return db.session.query(Clas).join(Finish, Finish.class_id == Clas.class_id).filter(
        func.to_days(Finish.time) == func.to_days(datetime.now())).all()


def query_student_by_student_number(student_number) -> Student:
    """
    根据学号查询学生信息
    :param student_number:
    :return:
    """
    global student_map
    if student_map is None:
        student_map = dict(map(lambda x: (x.student_number, x), get_student_info()))
    return student_map.get(student_number)


def convert_one_records_to_students(one_records: List) -> List[Student]:
    """
    将学号列表转换为学生信息列表
    :param one_records:
    :return:
    """
    res = []
    for record in one_records:
        # 查询数据库中的记录，主要是用来获取对应的qq号码
        db_record = query_student_by_student_number(int(record['jobNumber']))
        if db_record is None:
            # 如果查询不到对应的记录，则使用小one易打卡中的姓名
            # 密码字段为空
            db_record = Student()
            db_record.student_number = record['jobNumber']
            db_record.student_name = record['userName']
        res.append(db_record)
    return res


def get_cube_classes() -> List[Clas]:
    """
    请求所有的班级魔方班级
    :return:
    """
    return db.session.query(Clas).filter(Clas.cube_id.is_not(None)).all()
