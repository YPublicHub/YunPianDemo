import struct


class MessageHeader:
    def __init__(self,
                 bodylength,
                 command_id,
                 seq_id):
        self._total_length = struct.pack('!I', 12+bodylength)
        self._command_id = struct.pack('!I', command_id)
        self._seq_id = struct.pack('!I', seq_id)

    def total_length(self):
        return self._total_length

    def header(self):
        return self._total_length + self._command_id + self._seq_id



