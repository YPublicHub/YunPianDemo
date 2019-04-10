from src.cmpp import Cmpp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['POST'])
def send():
    print(request.form.get('username'))
    un = request.form.get('username')
    pwd = request.form.get('password')
    mobile = request.form.get('mobile')
    content = request.form.get('content')

    c = Cmpp('118.178.110.140', '30001', un, pwd, '0')
    f1 = c.connect_server()
    if f1 is False:
        return jsonify({'result': '连接cmpp服务器失败'})
    f2, conn_data = c.connect_application()
    if f2 is False:
        return jsonify({'result': '登陆cmpp失败，状态码为{}'.format(conn_data)})
    f3, send_data = c.send_message([mobile], content)
    if f3 is False:
        return jsonify({'result': '发送短信失败，状态码为{}'.format(send_data)})
    return jsonify({'result': 'ok'})



if __name__ == '__main__':
    app.run(port=5000)

