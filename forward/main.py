import random
from flask import Flask, request
from paho.mqtt import client as mqtt_client

import config


def connect_publish_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("mqtt服务器连接成功")
        else:
            print("mqtt连接失败！错误码： %d\n", rc)

    client_id = f'publish-{random.randint(0, 1000)}'
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(config.mqtt_broker, config.mqtt_port)
    return client


app = Flask(__name__)
pub_mqtt = connect_publish_mqtt()


@app.route('/', methods=["POST"])
def index():
    pub_mqtt.publish(topic=config.mqtt_topic, payload=request.data)

    return "None"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.http_listen_port)
