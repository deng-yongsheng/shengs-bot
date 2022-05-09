import requests
from . import config
from exceptions import MessageSendError


def send_private_msg(user_id, message, group_id=None, auto_escape=False):
    """
    发送私聊消息
    终结点：/send_private_msg
    :param user_id:对方 QQ 号
    :param message:要发送的内容
    :param group_id:主动发起临时会话群号(机器人本身必须是管理员/群主)
    :param auto_escape:消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
    :return:
    """
    query_url = '/send_private_msg'
    res = requests.get(config.GO_CQHTTP_URL + query_url, params={
        'user_id': user_id,
        'group_id': group_id,
        'message': message,
        'auto_escape': auto_escape
    })
    print('发送消息', res)
    if res.json()['status'] != 'ok':
        raise MessageSendError(res.text)


def send_group_msg(group_id, message, auto_escape=False):
    """
    发送私聊消息
    终结点：/send_group_msg
    :param group_id:	群号
    :param message:要发送的内容
    :param group_id:主动发起临时会话群号(机器人本身必须是管理员/群主)
    :param auto_escape:消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效
    :return:
    """
    query_url = '/send_group_msg'
    res = requests.get(config.GO_CQHTTP_URL + query_url, params={
        'group_id': group_id,
        'message': message,
        'auto_escape': auto_escape
    })
    print('发送群消息', res)
    if res.json()['status'] != 'ok':
        raise MessageSendError(res.text)
