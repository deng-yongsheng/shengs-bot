from datetime import datetime

import message
from exceptions import TokenExpire
from one.request import get_unreported_by_token
from one.service import get_counselor_by_name, convert_student_numbers_to_students


def get_one_report_for(counselor=None):
    """
    生成打卡报表
    :return:
    """
    assert counselor == '肖沫晔', '目前仅支持肖沫晔老师'
    counselor = get_counselor_by_name(counselor)
    try:
        unreported_student_numbers = get_unreported_by_token(token=counselor.token)
        manege_student_ids = []
        for cls in counselor.classes:
            manege_student_ids.extend(map(lambda x: x.student_number, cls.students))
        manege_student_ids = set(manege_student_ids)
        # 只保留管理的班级的学生记录
        his_student_number_list = []
        for one_record in unreported_student_numbers:
            if one_record['jobNumber'] and int(one_record['jobNumber']) in manege_student_ids:
                his_student_number_list.append(int(one_record['jobNumber']))
        his_student_list = convert_student_numbers_to_students(his_student_number_list)
        # 按班级归类
        form = dict.fromkeys(map(lambda x: x.class_name, counselor.classes))
        for stu in his_student_list:
            if form.get(stu._class.class_name) is None:
                form[stu._class.class_name] = []
            form[stu._class.class_name].append(stu)
        mess_list = []
        for cls, stu_list in form.items():
            if stu_list is not None:
                mess_list.append(f"{cls}：{'、'.join(map(lambda x: x.student_name, stu_list))}")
        date_str = datetime.now().strftime("%Y-%m-%d") + '打卡未完成人员名单：'
        # 发送私聊消息：日期
        message.send_private_msg(counselor.counselor_qq, date_str)
        # 发送私聊消息：名单
        mess = '\n'.join(mess_list)
        message.send_private_msg(counselor.counselor_qq, mess)
    except TokenExpire:
        # 发送私聊消息：名单
        teacher_call = counselor.counselor_name[0] + '老师'
        mess = f"{teacher_call}：\n您的小one易登录会话过期，请重新登录微信小one易"
        message.send_private_msg(counselor.counselor_qq, mess)


def alert_counselor():
    """
    对辅导员进行提醒
    :return:
    """
    get_one_report_for('肖沫晔')
