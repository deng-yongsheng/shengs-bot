import json

from paho.mqtt.client import MQTTMessage

import message
import message_type
from bot_reply import bot
from .mqtt import connect_mqtt, topic
from .scripts import 肖沫晔, 邓永盛, 所有群


def on_message(client, userdata, msg: MQTTMessage):
    """
    处理mqtt消息
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    try:
        res_j = json.loads(msg.payload)
        if 'post_type' in res_j and res_j['post_type'] == 'message':
            if res_j.get('message_type') == 'private':
                # 私聊信息
                p_message = message_type.PrivateMessage(res_j)
                print(p_message)
                reply = bot.handle_private_message(p_message)
                # 针对私聊消息进行回复
                if reply is not None:
                    message.send_private_msg(p_message.user_id, reply.reply)
                    return
            elif res_j.get('message_type') == 'group':
                # 群聊信息
                g_message = message_type.GroupMessage(res_j)
                print(g_message)
                reply = bot.handle_group_message(g_message)
                # 针对群消息进行回复
                if reply is not None:
                    message.send_group_msg(g_message.group_id, reply.reply)
                    return
            else:
                # 其它类型的消息
                # print(res_j)
                pass
    except json.JSONDecodeError:
        print('mqtt消息不规范')


mqtt = connect_mqtt()
mqtt.subscribe(topic)
mqtt.on_message = on_message


def run():
    """
    启动mqtt监听消息
    :return:
    """
    mqtt.loop_forever(timeout=1)
