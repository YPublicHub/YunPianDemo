import json
import urllib.parse
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)


def connect_db(host, port, user, pwd, db_name):
    connect = pymysql.Connect(
        host=host,
        port=port,
        user=user,
        passwd=pwd,
        db=db_name,
        charset='utf8'
    )
    cursor = connect.cursor()
    return connect, cursor


connect, cursor = connect_db('xxx', 3306, 'xxx', 'xxx', 'xxx')


@app.route('/msg_reply', methods=['POST'])
def msg_reply():
    """
    短信回复回调
    :return:
    """
    reply_data = request.form.get('sms_reply')
    reply_dict = json.loads(urllib.parse.unquote(reply_data))
    sql = 'INSERT INTO mesage_reply (mobile, reply_time, text) VALUES ( "{}", "{}", "{}" )'.format(
    reply_dict.get('mobile'), reply_dict.get('reply_time'), reply_dict.get('text'))
    cursor.execute(sql)
    connect.commit()
    return '0'


@app.route('/msg_status', methods=['POST'])
def msg_status():
    """
    短信状态回调
    :return:
    """
    status_data = request.form.get('sms_status')
    status_dict = json.loads(urllib.parse.unquote(status_data))
    print(status_dict)
    for d in status_dict:
        sql = 'INSERT INTO mesage_status (error_detail, sid, uid, user_receive_time, error_msg, mobile, report_status) ' \
              'VALUES ( "{}", "{}", "{}", "{}", "{}", "{}", "{}" )' \
            .format(d.get('error_detail'), d.get('sid'), d.get('uid'),
                    d.get('user_receive_time'), d.get('error_msg'), d.get('mobile'),
                    d.get('report_status'))
        cursor.execute(sql)
        connect.commit()
    return '0'


if __name__ == '__main__':
    connect, cursor = connect_db('xxx', 3306, 'xxx', 'xxx', 'xxx')
    app.run()
