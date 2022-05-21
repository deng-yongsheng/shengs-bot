from typing import List, Union, Dict, Callable
import message_type

# 群消息 通用 处理函数列表
common_group_handle_list: List[Callable] = []
# 群消息 特定群处理函数列表
certain_group_handle_dict: Dict[int, List[Callable]] = {}
# 私聊 通用 处理函数列表
common_private_handle_list: List[Callable] = []
# 私聊 特定人处理函数列表
certain_private_handle_dict: Dict[int, List[Callable]] = {}


def common_group_message_handler(func):
    """
    通用 群消息接收处理函数的装饰器
    :param func:
    :return:
    """
    common_group_handle_list.append(func)


def certain_group_message_handler(group_id: Union[int, List[int]] = None):
    """
    特定 群消息接收处理函数的装饰器
    :param group_id:
    :return:
    """
    print(f"为群{group_id}注册函数")

    def wrapper(func):
        if isinstance(group_id, int):
            if group_id not in certain_group_handle_dict:
                certain_group_handle_dict.update({group_id: []})
            certain_group_handle_dict[group_id].append(func)
        elif isinstance(group_id, List):
            assert all(map(lambda x: isinstance(x, int), group_id)), '群号必须是整数'
            # 装饰器参数：group_id
            for groupid in group_id:
                if groupid not in certain_group_handle_dict:
                    certain_group_handle_dict.update({groupid: []})
                else:
                    certain_group_handle_dict[groupid].append(func)
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


def certain_private_message_handler(qq_number: Union[int, List[int]] = None):
    """
    处理所有的私信消息
    :return:
    """
    print(f"为qq用户{qq_number}注册函数")

    def wrapper(func):
        if isinstance(qq_number, int):
            if qq_number not in certain_private_handle_dict:
                certain_private_handle_dict.update({qq_number: []})
            certain_private_handle_dict[qq_number].append(func)
        elif isinstance(qq_number, List):
            assert all(map(lambda x: isinstance(x, int), qq_number)), 'qq号必须是整数'
            for qq in qq_number:
                if qq not in certain_private_handle_dict:
                    certain_private_handle_dict.update({qq: []})
                else:
                    certain_private_handle_dict[qq].append(func)
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
    if group_message.group_id in certain_group_handle_dict:
        for handler in certain_group_handle_dict[group_message.group_id]:
            group_reply = handler(group_message)
            if group_reply is not None:
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
    if private_message.sender.user_id in certain_private_handle_dict:
        for handler in certain_private_handle_dict[private_message.user_id]:
            private_reply = handler(private_message)
            if private_reply is not None:
                return private_reply
    else:
        for private_handle in common_private_handle_list:
            private_reply = private_handle(private_message)
            if private_reply is not None and isinstance(private_reply, message_type.PrivateMessageReply):
                return private_reply
