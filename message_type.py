import datetime
from enum import Enum

TIME_ZONE_UTC_8 = datetime.timezone(datetime.timedelta(hours=8))


class EnumMessageType(Enum):
    private = 1
    group = 2


class EnumTempSource(Enum):
    """
    临时消息来源枚举
    """
    群聊 = 0
    QQ咨询 = 1
    查找 = 2
    QQ电影 = 3
    热聊 = 4
    验证消息 = 6
    多人聊天 = 7
    约会 = 8
    通讯录 = 9


class EnumSex(Enum):
    """
    性别枚举
    """
    unknown = 0
    male = 1
    female = 2


class EnumPostType(Enum):
    """
    消息种类，区分聊天、请求、提示
    """
    message = 1
    notice = 2
    request = 3


class EnumSubType(Enum):
    """
    群聊消息子类型
    """
    # 正常消息
    normal = 1
    # 匿名消息
    anonymous = 2
    # 系统提示
    notice = 3


class EnumGroupSenderRole(Enum):
    """
    群消息的发送人身份
    """
    member = 0  # 群成员
    admin = 1  # 群管理员
    owner = 2  # 群主
    __tostr_dict = {0: '群成员', 1: '群管理员', 2: '群主'}

    def to_str(self):
        return self.__tostr_dict[self.value]


class Sender:
    """
    消息发送人信息
    """
    user_id: int
    nickname: str
    sex: EnumSex
    age: int

    def __init__(self, s_sender: dict):
        for key, value in s_sender.items():
            self.__setattr__(key, value)
        self.sex = EnumSex[s_sender.get('sex')]

    def __repr__(self):
        return f"<QQ用户({self.user_id}) {self.nickname}>"


class PrivateSender(Sender):
    """
    私聊消息发送者
    """
    pass


class GroupSender(Sender):
    """
    群消息发送者
    """
    card: str
    area: str
    level: str
    role: EnumGroupSenderRole
    title: str

    def __init__(self, sender_dict):
        super(GroupSender, self).__init__(sender_dict)
        self.role = EnumGroupSenderRole[sender_dict.get('role')]

    def __repr__(self):
        return f"<群成员({self.user_id}) {self.nickname}>"


class MessageBase:
    """
    消息的父类
    """
    time: datetime.datetime
    self_id: int
    post_type: EnumPostType
    message_type: EnumMessageType
    sub_type: str
    temp_source: EnumTempSource
    message_id: int
    user_id: int
    message: str
    raw_message: str
    font: int
    sender: Sender

    def __init__(self, msg: dict):
        for key, value in msg.items():
            self.__setattr__(key, value)
        self.post_type = EnumPostType[msg.get('post_type')]
        self.message_type = EnumMessageType[msg.get('message_type')]
        self.time = datetime.datetime.fromtimestamp(msg.get('time'), TIME_ZONE_UTC_8)
        self.temp_source = msg.get('temp_source') and EnumTempSource[msg.get('temp_source')]
        self.sender = Sender(msg.get('sender'))

    def __repr__(self):
        return f"<聊天记录 {self.time.strftime('%Y-%m-%d %H:%M:%S')} ({self.user_id}):{self.raw_message} >"


class PrivateMessage(MessageBase):
    """
    私聊消息的实体
    """
    sender: PrivateSender

    def __init__(self, msg: dict):
        super(PrivateMessage, self).__init__(msg)

    def __repr__(self):
        un_return_message = self.message.replace('\n', ' ')
        return f"《好友消息({self.sender.nickname})：{un_return_message}》"


class GroupMessage(MessageBase):
    """
    群聊消息
    """
    group_id: int
    anonymous: dict
    sender: GroupSender
    sender_name: str

    def __init__(self, msg: dict):
        super(GroupMessage, self).__init__(msg)
        self.sender = GroupSender(msg.get('sender'))
        self.sender_name = self.sender.card or self.sender.nickname

    def __repr__(self):
        un_return_message = self.message.replace('\n', ' ')
        return f"《群聊消息({self.sender_name}) in ({self.group_id})：{un_return_message}》"


class MessageReplyBase:
    """
    消息回复基类
    """
    # 要回复的内容
    reply: str
    # 消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 reply 字段是字符串时有效
    auto_escape: bool

    def __repr__(self):
        return f"<消息回复 {self.reply}>"

    @property
    def json(self):
        raise RuntimeError('必须重置此函数')


class PrivateMessageReply(MessageReplyBase):
    """
    私聊消息回复
    """

    def __repr__(self):
        return f"<私聊消息回复 {self.reply}>"

    def __init__(self, reply: str = None, auto_escape: bool = False):
        """
        要回复的内容
        :param reply:
        :param auto_escape:
        :return:
        """
        self.reply = reply
        self.auto_escape = auto_escape

    @property
    def json(self):
        return {'reply': self.reply, 'auto_escape': self.auto_escape}


class GroupMessageReply(MessageReplyBase):
    """
    群聊消息回复
    """

    def __repr__(self):
        return f"<群聊消息回复 {self.reply}>"

    @property
    def json(self):
        return {'reply': self.reply, 'auto_escape': self.auto_escape}
