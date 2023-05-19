import uuid

from flask import Flask, jsonify
from CONFIG import server_ip, server_port,productionMode
from handler import  user, api, captcha

app = Flask(__name__)


app.debug = not productionMode
app.config['SECRET_KEY'] = b'45r3aug435qy95t3hu9pg4tyui4teabyiuybuegrbergrgiuhpergauh'

# 注册蓝图
app.register_blueprint(user.bp)
app.register_blueprint(api.bp)
app.register_blueprint(captcha.bp)

# 设置500错误处理器
@app.errorhandler(500)
def server_error(e):
    return jsonify({"code": 500, "msg": "Server Internal Error", "error": e, 'requestID': uuid.uuid4()})

# 设置405错误处理器
@app.errorhandler(405)
def server_error(e):
    return jsonify({"code": 405, "msg": "Method Not Allowed", 'requestID': uuid.uuid4()})

# 设置404错误处理器
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"code": 404, "msg": "Not Found", "error": None, 'requestID': uuid.uuid4()})


# 启动服务器程序
if __name__ == '__main__':
    app.run(host=server_ip, port=server_port)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
