import time
import traceback

import request
import service
import exceptions
from message import open_all_windows, send_qq_with_at

if __name__ == '__main__':
    # 打开所有的qq窗口
    open_all_windows()
    # 遍历班级
    for clas in service.get_class_to_prompt():
        print("*" * 40)
        try:
            print(clas.class_name)
            # 获取未完成打卡成员学号列表
            unreported_numbers = request.get_unreported(clas=clas)
            if len(unreported_numbers) > 0:
                # 将学号列表转学生信息列表
                unreported_students = service.convert_numbers_to_students(unreported_numbers)
                # 是否添加 可爱的xx
                if_cute = '可爱' if len(unreported_numbers) <= 4 else ''
                mess = '请' + if_cute + '、'.join(map(lambda x: x.student_name, unreported_students)) + "尽快完成小one易健康打卡"
                print(mess)
                # 发送消息
                send_qq_with_at(to_who=clas.class_group_name, msg=mess, at_list=unreported_students)
            else:
                # 记录班级打卡完成
                print(f'{clas.class_name} 打卡完毕！')
                service.class_finished(class_=clas)
        except exceptions.TokenExpire:
            mess = f'{clas.class_name}token失效，请班级管理员 {clas.token.admin_name} 重新打开小one易并登录。'
            print(mess)
            send_qq_with_at(clas.class_group_name)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            continue
    print('*' * 60)
    print('以下班级已经完成打卡，今天不再发送消息提醒：')
    for clas in service.get_finished_class_list():
        print(clas)
    time.sleep(5)
