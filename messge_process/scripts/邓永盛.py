from ..bot import specified_private_message_handler
from ..message_type import PrivateMessageReply, PrivateMessage


@specified_private_message_handler(1596953204)
def repeat(message: PrivateMessage):
    print("脚本处理消息")
    reply = PrivateMessageReply(reply=message.raw_message)
    return reply


print("脚本被加载")
