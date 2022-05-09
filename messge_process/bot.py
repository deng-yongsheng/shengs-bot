from typing import List, Union
from . import message_type

# 群消息 通用 处理函数列表
common_group_handle_list = []
# 群消息 特定群处理函数列表
specified_group_handle_dict = {}
# 私聊 通用 处理函数列表
common_private_handle_list = []
# 私聊 特定人处理函数列表
specified_private_handle_dict = {}


def common_group_message_handler(func):
    """
    通用 群消息接收处理函数的装饰器
    :param func:
    :return:
    """
    common_group_handle_list.append(func)


def specified_group_message_handler(group_id: Union[int, List[int]] = None):
    """
    特定 群消息接收处理函数的装饰器
    :param group_id:
    :return:
    """
    print(f"为群 {group_id}注册函数")

    def wrapper(func):
        if isinstance(group_id, int):
            specified_group_handle_dict.update({group_id: func})
        elif isinstance(group_id, List):
            assert all(map(lambda x: isinstance(x, int), group_id)), '群号必须是整数'
            # 装饰器参数：group_id
            handlers = dict.fromkeys(group_id, func)
            specified_group_handle_dict.update(handlers)
        else:
            raise AssertionError('群号必须是整数')

    return wrapper


def common_private_message_handler(func):
    """
    通用私聊消息 接收处理函数的装饰器
    :param func:
    :return:
    """
    common_private_handle_list.append(func)


def specified_private_message_handler(qq_number: Union[int, List[int]] = None):
    """
    处理所有的
    :return:
    """
    print(f"为qq用户 {qq_number}注册函数")

    def wrapper(func):
        if isinstance(qq_number, int):
            specified_private_handle_dict.update({qq_number: func})
        elif isinstance(qq_number, List):
            assert all(map(lambda x: isinstance(x, int), qq_number)), 'qq号必须是整数'
            handlers = dict.fromkeys(qq_number, func)
            specified_private_handle_dict.update(handlers)
        else:
            raise AssertionError('qq号必须是整数')

    return wrapper


def handle_group_message(group_message: message_type.GroupMessage):
    """
    处理群消息
    :param group_message:
    :return:
    """
    # 优先处理特定群消息
    if group_message.group_id in specified_group_handle_dict:
        group_reply = specified_group_handle_dict[group_message.group_id](group_message)
        return group_reply
    else:
        for group_handle in common_group_handle_list:
            group_reply = group_handle(group_message)
            if group_reply is not None and isinstance(group_reply, message_type.GroupMessageReply):
                return group_reply


def handle_private_message(private_message: message_type.PrivateMessage):
    """
    处理私聊
    :param private_message:
    :return:
    """
    # 优先处理特定qq用户消息
    if private_message.sender.user_id in specified_private_handle_dict:
        private_reply = specified_private_handle_dict[private_message.sender.user_id](private_message)
        return private_reply
    else:
        for private_handle in common_private_handle_list:
            private_reply = private_handle(private_message)
            if private_reply is not None and isinstance(private_reply, message_type.PrivateMessageReply):
                return private_reply
