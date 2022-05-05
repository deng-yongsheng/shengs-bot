class TokenExpire(Exception):
    """
    token过期异常
    """
    def __init__(self):
        self.msg = 'token过期'
