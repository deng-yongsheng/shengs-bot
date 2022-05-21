from ..bot import certain_private_message_handler
from message_type import PrivateMessageReply, PrivateMessage


@certain_private_message_handler(1596953204)
def repeat(message: PrivateMessage):
    if message.raw_message == 'ping':
        reply = PrivateMessageReply(reply='pong')
    else:
        reply = None
    return reply


@certain_private_message_handler(1596953204)
def make_response(message: PrivateMessage):
    import threading
    import os
    if message.raw_message == '打卡情况':
        reply = PrivateMessageReply('正在查询小one易打卡情况')
        # 使用os.system 防止数据库长时间连接导致断开
        thread = threading.Thread(target=os.system, args=('python main.py one counselor',))
        thread.start()
    else:
        reply = None
    return reply
