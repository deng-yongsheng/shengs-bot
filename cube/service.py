from typing import List

from db import Clas


def get_cube_classes() -> List[Clas]:
    """
    请求所有的班级魔方班级
    :return:
    """
    return db.session.query(Clas).filter(Clas.cube_id.is_not(None)).all()
