import time
import struct
import hashlib


class CmppConnectApp:
    def __init__(self,
                 sp_id,
                 sp_pwd,
                 version=struct.pack('!B', 0x21),
                 ):
        self._source_addr = sp_id.encode()
        self._secret = sp_pwd.encode()
        self._version = version
        self._timestamp = struct.pack('!L', int(time.strftime('%m%d%H%M%S', time.localtime(time.time()))))
        self._auth = hashlib.md5((self._source_addr + 9 * b'\x00' + self._secret + time.strftime('%m%d%H%M%S',time.localtime(time.time())).encode())).digest()
        self._length = 6 + 16 + 4 + 1
        self._body = (self._source_addr + self._auth + self._version + self._timestamp)

    def body(self):
        return self._body

    def body_len(self):
        return self._length


class CmppSubmit:
    def __init__(self,
                 pk_total,
                 pk_number,
                 registered_delivery,
                 msg_level,
                 service_id,
                 fee_user_type,
                 fee_teminal_id,
                 tp_pid,
                 tp_udhi,
                 msg_fmt,
                 msg_src,
                 fee_type,
                 fee_code,
                 valid_time,
                 at_time,
                 src_id,
                 dest_user_tl,
                 dest_teminal_id,
                 msg_length,
                 msg_content,
                 ):
        self._msg_id = 8 * b'\x00'
        self._pk_total = struct.pack('!B', pk_total)
        self._pk_number = struct.pack('!B', pk_number)
        self._registered_delivery = struct.pack('!B', registered_delivery)
        self._msg_level = struct.pack('!B', msg_level)
        self._service_id = service_id.encode()
        self._fee_user_type = struct.pack('!B', fee_user_type)
        self._fee_teminal_id = ('%021d' % fee_teminal_id).encode()
        self._tp_pid = struct.pack('!B', tp_pid)
        self._tp_udhi = struct.pack('!B', tp_udhi)
        self._msg_fmt = struct.pack('!B', msg_fmt)
        self._msg_src = msg_src.encode()
        self._fee_type = fee_type.encode()
        self._fee_code = fee_code.encode()
        self._valid_time = valid_time.encode()
        self._at_time = at_time.encode()
        self._src_id = (src_id + (21 - len(src_id)) * '\x00').encode()
        self._dest_user_tl = struct.pack('!B', dest_user_tl)
        self._dest_teminal_id = b''
        for v in dest_teminal_id:
            self._dest_teminal_id += (v + (21 - len(v)) * '\x00').encode()
        self._msg_length = struct.pack('!B', msg_length)
        self._msg_content = msg_content.encode('utf-16-be')
        self._reserve = 8 * b'\x00'
        self._body = self._msg_id + self._pk_total + self._pk_number + self._registered_delivery \
                     + self._msg_level + self._service_id + self._fee_user_type + self._fee_teminal_id \
                     + self._tp_pid + self._tp_udhi + self._msg_fmt + self._msg_src + self._fee_type \
                     + self._fee_code + self._valid_time + self._at_time + self._src_id + self._dest_user_tl \
                     + self._dest_teminal_id + self._msg_length + self._msg_content + self._reserve

        self._length = 126 + 21 * dest_user_tl + msg_length

    def body(self):
        return self._body

    def length(self):
        return self._length


