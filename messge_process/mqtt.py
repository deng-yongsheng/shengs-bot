import random
from paho.mqtt import client as mqtt_client

broker = '192.168.1.20'
port = 1883
topic = "/sheng-bot"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("mqtt服务器连接成功")
        else:
            print("mqtt连接失败！错误码： %d\n", rc)

    client_id = f'publish-{random.randint(0, 1000)}'
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
