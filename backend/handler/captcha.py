import hmac
import json

import requests
from CONFIG import geetestID, geetestKey, geetestEnabled
from flask import jsonify, Blueprint, request
import uuid

bp = Blueprint('captcha', __name__)


@bp.route('/api/captcha/verify', methods=['POST'])
def verify():
    if geetestEnabled:
        api_server = 'http://gcaptcha4.geetest.com'
        a = request.get_json()
        lot_number = a.get('lot_number')
        captcha_output = a.get('captcha_output')
        pass_token = a.get('pass_token')
        gen_time = a.get('gen_time')
        lotnumber_bytes = lot_number.encode()
        prikey_bytes = geetestKey.encode()
        sign_token = hmac.new(prikey_bytes, lotnumber_bytes, digestmod='SHA256').hexdigest()
        query = {
            "lot_number": lot_number,
            "captcha_output": captcha_output,
            "pass_token": pass_token,
            "gen_time": gen_time,
            "sign_token": sign_token,
        }
        url = api_server + '/validate' + '?captcha_id={}'.format(geetestID)
        try:
            res = requests.post(url, query)
            assert res.status_code == 200
            b = json.loads(res.text)
        except:
            b = {'result': 'success', 'reason': 'request geetest api fail'}
        if b['result'] == 'success':
            return jsonify({'code': 0, 'msg': '验证通过', 'requestID': uuid.uuid4()})
        else:
            return jsonify({'code': 407, 'msg': b['reason'], 'requestID': uuid.uuid4()})
    else:
        return jsonify({'code': 400, 'msg': '验证码服务未启用', 'requestID': uuid.uuid4()})
