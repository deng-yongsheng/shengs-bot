from ..bot import specified_private_message_handler
from ..message_type import PrivateMessageReply, PrivateMessage


@specified_private_message_handler(1596953204)
def repeat(message: PrivateMessage):
    if message.raw_message == 'ping':
        reply = PrivateMessageReply(reply='pong')
    else:
        reply = None
    return reply


print(__name__, "脚本被加载")
