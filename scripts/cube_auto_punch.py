from tqdm import tqdm

import db
import request.cube as cube


def auto_punch(punch_url):
    """
    修改班级魔方打卡状态
    :param punch_url:
    :return:
    """
    for auto_punch_record in tqdm(db.session.query(db.CubeAutoPunch).all()):
        auto_punch_record: db.CubeAutoPunch
        try:
            if auto_punch_record.skip == '否':
                cube.set_punch_state(punch_url, auto_punch_record)
        except Exception as e:
            print('打卡状态修改失败')
            print(e)


if __name__ == '__main__':
    print('修改打卡状态')
    punch_list = cube.get_cur_punch_url()
    for punch_url in punch_list:
        auto_punch(punch_url)
