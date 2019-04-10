import socket
import struct
from src.cmpp_resp import Response
from src.cmpp_header import MessageHeader
from src.cmpp_service import CmppConnectApp, CmppSubmit


class Cmpp:
    def __init__(self,
                 gateway,
                 port,
                 sp_id,
                 sp_pwd,
                 src_id,
                 ):
        """

        :param gateway: 网关ip
        :param port: 网关端口号
        :param sp_id: 企业的原地址
        :param sp_pwd: 企业与中国移动约定的密码
        :param src_id: 源号码，最终显示在用户手机上的号码
        """
        self._gateway = gateway
        self._port = port
        self._sp_id = sp_id
        self._sp_pwd = sp_pwd
        self._src_id = src_id
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._parse = Response()
        self._client.settimeout(3)

    def connect_server(self):
        try:
            self._client.connect((self._gateway, int(self._port)))
        except Exception as e:
            return False
        else:
            return True

    def disconnect_server(self):
        try:
            self._client.close()
        except Exception as e:
            exit(-1)

    def connect_application(self):
        try:
            conn_body = CmppConnectApp(self._sp_id, self._sp_pwd)
            conn_header = MessageHeader(conn_body.body_len(), 0x00000001, 0)
            conn_msg = conn_header.header() + conn_body.body()
            self._client.send(conn_msg)
            length = self._client.recv(4)
            total_length = struct.unpack('!L', length)[0]
            self._parse.parse(length + self._client.recv(total_length - 4))
            body = self._parse.resp_body('connect_app')
            if body['status'] != 0:
                self.disconnect_server()
                return False, body['status']
        except Exception as e:
            return False, '登陆超时'
        else:
            return True, body['status']

    def send_message(self, phone, content):
        try:
            submit_body = CmppSubmit(pk_total=1,
                                     pk_number=1,
                                     registered_delivery=0,
                                     msg_level=0,
                                     service_id='MJS0019905',
                                     fee_user_type=2,
                                     fee_teminal_id=0,
                                     tp_pid=0,
                                     tp_udhi=0,
                                     msg_fmt=8,
                                     fee_type='01',
                                     fee_code='000000',
                                     valid_time=17*'\x00',
                                     at_time=17*'\x00',
                                     msg_src=self._sp_id,
                                     dest_user_tl=len(phone),
                                     dest_teminal_id=phone,
                                     msg_length=len(content)*2,
                                     msg_content=content,
                                     src_id=self._src_id)
            submit_header = MessageHeader(submit_body.length(), 0x00000004, 0)
            submit_msg = submit_header.header() + submit_body.body()
            self._client.send(submit_msg)
            length = self._client.recv(4)
            total_length = struct.unpack('!L', length)[0]
            self._parse.parse(length + self._client.recv(total_length - 4))
            body = self._parse.resp_body('submit')
            if body['result'] != 0:
                return False, body['result']
        except Exception as e:
            print(e)
            return False, '发送超时'
        else:
            return True, body['result']




