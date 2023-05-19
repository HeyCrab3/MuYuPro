import base64
import datetime
import json

from flask import Flask, render_template, jsonify, Blueprint, redirect, request, session
from db import db
from bson import json_util
import uuid

def parse_json(data):
    return json.loads(json_util.dumps(data))

bp = Blueprint('user', __name__)


def find(phone):
    users = list(db.user.find({'phone': phone}))
    for user in users:
        if user['phone'] == phone:
            return user
    return None


def parse_json(data):
    return json.loads(json_util.dumps(data))

@bp.route('/api/user/info')
def userInfo():
    try:
        s = base64.b64decode(session['user']).decode('utf-8')
        result = find(s)
        result = parse_json(result)
        if result:
            return jsonify({'code': 0, 'msg': '操作成功', 'data': result, 'requestID': uuid.uuid4()})
        else:
            return jsonify({'code': 400, 'msg': '用户不存在或没有完成注册流程', 'requestID': uuid.uuid4()})
    except:
        return jsonify({'code': 401, 'msg': '未登录', 'requestID': uuid.uuid4()})

@bp.route('/api/user/login', methods=['POST'])
def login():
    a = request.get_json()
    phone_number = a['phone']
    sms_code = int(a['sms_code'])
    isExpired = db.code.find_one({'code': sms_code, 'phone': phone_number})
    if isExpired:
        if isExpired['expires_on'] <= int(datetime.datetime.now().timestamp()):
            return jsonify({'code': 400, 'msg': '验证码已过期', 'requestID': uuid.uuid4()})
        else:
            result = find(phone_number)
            if result:
                session['user'] = base64.b64encode(bytes(phone_number.encode('utf-8')))
                return jsonify({'code': 0, 'msg': '登陆成功', 'requestID': uuid.uuid4()})
            else:
                session['user'] = base64.b64encode(bytes(phone_number.encode('utf-8')))
                return jsonify({'code': 1, 'msg': '欢迎加入，请先介绍一下自己吧', 'requestID': uuid.uuid4()})
    else:
        return jsonify({'code': 400, 'msg': '验证码不存在', 'requestID': uuid.uuid4()})

@bp.route('/api/user/register', methods=['POST'])
def register():
    try:
        a = request.get_json()
        s = base64.b64decode(session['user']).decode('utf-8')
        result = find(s)
        if result:
            return jsonify({'code': 400, 'msg': '你在干什么？', 'requestID': uuid.uuid4()})
        else:
            db.user.insert_one({
                'phone': s,
                'nick': a['nick'],
                'avatar': a['avatar'],
                'point': 0
            })
            return jsonify({'code': 0, 'msg': '注册成功', 'requestID': uuid.uuid4()})
    except:
        return jsonify({'code': 401, 'msg': '未登录', 'requestID': uuid.uuid4()})