import threading

from ..bot import specified_private_message_handler
from ..message_type import PrivateMessageReply, PrivateMessage
import one as p_one


@specified_private_message_handler(2694607943)
def make_response(message: PrivateMessage):
    if message.raw_message == '打卡情况':
        reply = PrivateMessageReply('正在查询小one易打卡情况')
        thread = threading.Thread(target=p_one.get_one_report_for, args=('肖沫晔',))
        thread.start()
    else:
        reply = None
    return reply
