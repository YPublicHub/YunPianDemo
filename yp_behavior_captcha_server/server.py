import yaml
import json
import time
import random
import hashlib
import requests
from flask import Flask, render_template, request, jsonify

auth_num = None
reg_flag = False
app = Flask(__name__)


def get_config():
    with open('./config.yaml') as f:
        conf = yaml.load(f)

    return conf

conf = get_config()
print(type(conf))

@app.route('/')
def index():
    global reg_flag
    reg_flag = False
    return render_template('xwyz.html', cid=conf['captchaId'])


@app.route('/back', methods=['POST'])
def back():
    print(request.form)
    data = {
        'captchaId': request.form.get('captchaId'),
        'token': request.form.get('token'),
        'authenticate': request.form.get('authenticate'),
        'secretId': conf['secretId'],
        'version': '1.0',
        'timestamp': int(time.time() * 1000),
        'nonce': random.randint(1, 99999)
    }
    field = []
    for k in data.keys():
        field.append(k)
    field_sorted = sorted(field)
    t = ''
    for k in field_sorted:
        t += k
        t += str(data[k])
    t += conf['secretKey']
    print(t)
    md5 = hashlib.md5()
    md5.update(t.encode())
    data['signature'] = md5.hexdigest()
    r = requests.post('https://captcha.yunpian.com/v1/api/authenticate', data=data)
    print(r.text)
    if json.loads(r.text)['code'] == 0:
        global reg_flag
        reg_flag = True
        return jsonify({'code': 0, 'msg': 'ok'})
    else:
        return jsonify({'code': json.loads(r.text)['code'], 'msg': json.loads(r.text)['msg']})


@app.route('/reg', methods=['POST'])
def reg():
    global reg_flag
    if reg_flag and request.form.get('yzm') == str(auth_num):
        reg_flag = False
        return '注册成功'
    else:
        return '注册验证失败'


@app.route('/send', methods=['POST'])
def send():
    global auth_num
    if reg_flag is False:
        return '请先完成行为认证，再发送验证码'
    num = random.randint(1000, 9999)
    data = {
        'apikey': conf['apikey'],
        'mobile': request.form.get('phone'),
        'text': conf['template'].format(num)
    }
    r = requests.post('https://sms.yunpian.com/v2/sms/single_send.json', data=data)
    if json.loads(r.text)['code'] == 0:
        auth_num = num
        return '验证码发送成功'
    else:
        return '验证码发送失败,{}'.format(json.loads(r.text)['msg'])


if __name__ == '__main__':
    conf = get_config()
    app.run(host='0.0.0.0', port=5000)
