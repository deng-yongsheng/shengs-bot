from tqdm import tqdm

import db
from exceptions import exception_handler
from . import request


@exception_handler
def auto_punch(punch_url=None):
    """
    修改班级魔方打卡状态
    :param punch_url:
    :return:
    """
    if punch_url is None:
        # 获取当前打卡列表
        punch_url_list = request.get_cur_punch_url_list()
    else:
        # 来自函数形参
        punch_url_list = [punch_url]
    print(f'共要进行{len(punch_url_list)}项打卡')
    for punch_url in punch_url_list:
        for auto_punch_record in tqdm(db.session.query(db.CubeAutoPunch).all()):
            auto_punch_record: db.CubeAutoPunch
            try:
                if auto_punch_record.skip == '否':
                    request.set_punch_state(punch_url, auto_punch_record)
            except Exception as e:
                print('打卡状态修改失败')
                print(e)
