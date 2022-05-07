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
