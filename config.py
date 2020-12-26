import codecs
import struct

import dataclasses as dataclasses

host = '25.45.173.121'
port = 5005
ip_start = host[:host.rfind('.') + 1]

ip_range_list = ['{}{}'.format(ip_start, x) for x in range(0, 256)]

ip_range_list.append('25.45.173.121')


@dataclasses.dataclass
class Msg:
    Magic_cookie: int
    Message_type: int
    Server_port: int

    def get_port_as_bytes(self):
        return self.Server_port

    def get_Message_type(self):
        return self.Message_type

    def get_Magic_cookie(self):
        return self.Magic_cookie

    def msg_to_bytes(self):
        MESSAGE = str(hex(self.Magic_cookie)) + str(hex(self.Message_type)) + str(hex((self.Server_port)))
        return bytes(MESSAGE, 'utf-8')

def bytes_to_msg(bytes):
        msg_type = bytes[:4]
        msg_data = bytes[5:7]
        port = bytes[8::]
        return msg_type.decode("utf-8"), msg_data.deocde("utf-8"), port.decode("utf-8")