import datetime
import json
import random

from flask import jsonify, Blueprint, request
import uuid
from db import db
from CONFIG import tencentCloudSecretKey, tencentCloudSecretID, smsTemplateID, smsAppSdkId, signName, expiresOn
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

bp = Blueprint('api', __name__)

@bp.route('/api/sms/send', methods=['POST'])
def sendSMS():
    if tencentCloudSecretID == "" or tencentCloudSecretKey == "" or smsTemplateID == "" or smsAppSdkId == "" or signName == "":
        return jsonify({'code': 500, 'msg': '后端数据未填写完成，请联系管理员', 'requestID': uuid.uuid4()})
    else:
        a = request.get_json()
        if a['phone'] == "":
            return jsonify({'code': 400, 'msg': '你在干什么？', 'requestID': uuid.uuid4()})
        else:
            try:
                # 初始化参数
                sms_code = random.randint(100000, 1000000)
                # 初始化凭据
                cred = credential.Credential(tencentCloudSecretID, tencentCloudSecretKey)

                # 初始化 httpProfile
                httpProfile = HttpProfile()
                httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
                httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒(默认60秒)
                httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

                # 初始化 clientProfile
                clientProfile = ClientProfile()
                clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
                clientProfile.language = "en-US"
                clientProfile.httpProfile = httpProfile

                # 请求模块
                client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)
                req = models.SendSmsRequest()
                params = {
                    "PhoneNumberSet": [a['phone']],
                    "SmsSdkAppId": smsAppSdkId,
                    "SignName": signName,
                    "TemplateId": smsTemplateID,
                    "TemplateParamSet": [str(sms_code), str(int(expiresOn / 60))]
                }
                req.from_json_string(json.dumps(params))
                # 发送短信
                resp = client.SendSms(req)
                if json.loads(resp.to_json_string(indent=2))['SendStatusSet'][0]['Code'] != "Ok":
                    return jsonify({'code': 500, 'requestID': uuid.uuid4(), 'msg': json.loads(resp.to_json_string(indent=2))['SendStatusSet'][0]['Code']})
                else:
                    db.code.insert_one({
                        'phone': a['phone'],
                        'code': sms_code,
                        'expires_on': int(datetime.datetime.now().timestamp()) + expiresOn
                    })
                    return jsonify({'code': 0, 'requestID': uuid.uuid4(), 'msg': '验证码发送成功'})

            except TencentCloudSDKException as err: # 错误处理
                # 当出现以下错误码时，快速解决方案参考
                # - [FailedOperation.SignatureIncorrectOrUnapproved](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Afailedoperation.signatureincorrectorunapproved-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
                # - [FailedOperation.TemplateIncorrectOrUnapproved](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Afailedoperation.templateincorrectorunapproved-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
                # - [UnauthorizedOperation.SmsSdkAppIdVerifyFail](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Aunauthorizedoperation.smssdkappidverifyfail-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
                # - [UnsupportedOperation.ContainDomesticAndInternationalPhoneNumber](https://cloud.tencent.com/document/product/382/9558#.E7.9F.AD.E4.BF.A1.E5.8F.91.E9.80.81.E6.8F.90.E7.A4.BA.EF.BC.9Aunsupportedoperation.containdomesticandinternationalphonenumber-.E5.A6.82.E4.BD.95.E5.A4.84.E7.90.86.EF.BC.9F)
                # - 更多错误，可咨询[腾讯云助手](https://tccc.qcloud.com/web/im/index.html#/chat?webAppId=8fa15978f85cb41f7e2ea36920cb3ae1&title=Sms)
                return jsonify({'code': 500, 'msg': '服务器错误','error': str(err), 'requestID': uuid.uuid4()})