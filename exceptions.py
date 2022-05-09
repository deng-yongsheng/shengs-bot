class TokenExpire(Exception):
    """
    token过期异常
    """

    def __init__(self):
        self.msg = 'token过期'


class MessageSendError(Exception):
    """
    qq消息发送异常
    """

    def __init__(self, msg):
        self.msg = msg


class StudentNotInDatabase(Exception):
    """
    数据库中没有对应学生的记录
    """

    def __init__(self, msg):
        self.msg = msg


def exception_handler(func):
    import traceback
    import sys

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            exception_info = traceback.format_exc()
            sys.stderr.write(exception_info)
            # 将错误写入文件
            with open('exception.log', 'w', encoding='utf8') as f:
                f.write(exception_info)

    return wrapper
