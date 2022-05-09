from flask import Flask, request
from . import configs, message_type
from .exts import db
from . import bot
from .scripts.邓永盛 import *

app = Flask(__name__)
# 加载配置文件
app.config.from_object(configs)
# db绑定app
db.init_app(app)


def load_scripts():
    import glob, os
    current_path = os.path.basename(os.path.realpath(__file__))
    for file in glob.glob(current_path + 'scripts/*.py'):
        exec(file)


@app.route('/', methods=["POST"])
def post_data():
    if request.json is not None:
        if 'post_type' in request.json and request.json['post_type'] == 'message':
            if request.json.get('message_type') == 'private':
                # 私聊信息
                p_message = message_type.PrivateMessage(request.json)
                print(p_message)
                bot.handle_private_message(p_message)
            elif request.json.get('message_type') == 'group':
                # 群聊信息
                g_message = message_type.GroupMessage(request.json)
                print(g_message)
                bot.handle_group_message(g_message)
            else:
                # 其它类型的消息
                print(request.json)
    return 'None'

# load_scripts()
