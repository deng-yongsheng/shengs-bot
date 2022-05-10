from ..bot import common_group_message_handler
from message_type import GroupMessageReply, GroupMessage


@common_group_message_handler
def ping_pong(message: GroupMessage):
    """
    在收到ping 的时候回复pong
    :param message:
    :return:
    """
    if message.raw_message == 'ping':
        reply = GroupMessageReply(reply='pong')
    else:
        reply = None
    return reply

