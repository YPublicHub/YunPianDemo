import struct


class Response:
    def __init__(self):
        self._header = b''
        self._body = b''
        self._body_length = 0
        self._total_length = 12
        self._command_id = 0
        self._seq_id = 0
        self._resp_type = {
            'connect_app': ConnectAppPaser(),
            'submit': SubmitParse(),
        }

    def parse(self, resp):
        self._total_length = struct.unpack('!L', (resp[0:4]))
        self._command_id = struct.unpack('!L', resp[4:8])
        self._seq_id = struct.unpack('!L', resp[8:12])
        self._body = resp[12:self._total_length[0]]

    def resp_body(self, type):
        return self._resp_type[type].parse(self._body)


class ConnectAppPaser:

    def parse(self, body):
        return {
            'status': struct.unpack('!B', body[0:1])[0],
            'auth': body[1:17],
            'version': struct.unpack('!B', body[17:18])[0]
        }


class SubmitParse:

    def parse(self, body):
        return {
            'msg_id': body[0:8],
            'result': struct.unpack('!B', body[8:9])[0]
        }


