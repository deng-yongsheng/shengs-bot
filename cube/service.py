from typing import List

import db
from db import Clas, Student


def query_class_by_cube_id(cube_id: int) -> Clas:
    """
    根据班级魔方的班级id查对应班级
    :param cube_id: 班级魔方id
    :return: 对应班级
    """
    with db.DBSession() as session:
        return session.query(Clas).filter(Clas.cube_id == int(cube_id)).one_or_none()


def query_student_by_cube_id(cube_id: int) -> Student:
    """
    根据班级魔方的班级id查对应学生
    :param cube_id: 班级魔方id
    :return: 对应班级
    """
    with db.DBSession() as session:
        return session.query(Student).filter(Student.cube_id == int(cube_id)).one_or_none()


def get_cube_classes() -> List[Clas]:
    """
    请求所有的班级魔方班级
    :return:
    """
    with db.DBSession() as session:
        return session.query(Clas).filter(Clas.cube_id.is_not(None)).all()
