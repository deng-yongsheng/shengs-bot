import traceback

import request
import service
import exceptions
from message import send_qq_with_at


def alert_classes(debug=False):
    """
    进行班级提醒
    :return:
    """
    # 遍历班级
    for clas in service.get_class_to_prompt():
        print("*" * 40)
        try:
            print(clas.class_name)
            # 获取未完成打卡成员学号列表
            unreported_numbers = request.one.get_unreported(clas=clas)
            if len(unreported_numbers) > 0:
                # 将学号列表转学生信息列表
                unreported_students = service.convert_numbers_to_students(unreported_numbers)
                # 是否添加 可爱的xx
                if_cute = '可爱' if len(unreported_numbers) <= 4 else ''
                mess = '请' + if_cute + '、'.join(map(lambda x: x.student_name, unreported_students)) + "尽快完成小one易健康打卡\n"
                print(mess.replace('\n', ''))
                # 发送消息
                if not debug:
                    send_qq_with_at(to_who=clas.class_group_name, msg=mess, at_list=unreported_students)
            else:
                # 记录班级打卡完成
                print(f'{clas.class_name} 打卡完毕！')
                service.class_finished(class_=clas)
        except exceptions.TokenExpire:
            # 提醒对应班级token失效
            mess = f'{clas.class_name}token失效，请班级管理员 {clas.token.admin_name} 重新打开小one易并登录。'
            print(mess)
            if not debug:
                send_qq_with_at(clas.class_group_name, msg=mess)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            continue
    print('*' * 60)
    print('以下班级已经完成打卡，今天不再发送消息提醒：')
    for clas in service.get_finished_class_list():
        print(clas)


def alert_counselors():
    """
    对辅导员进行提醒
    :return:
    """
    pass
