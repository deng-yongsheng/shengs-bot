from flask import Flask, request, jsonify

from mqtt import connect_publish_mqtt, topic

app = Flask(__name__)
pub_mqtt = connect_publish_mqtt()


@app.route('/', methods=["POST"])
def index():
    pub_mqtt.publish(topic=topic, payload=request.data)

    return "None"
