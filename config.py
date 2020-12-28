import codecs
import struct

import dataclasses as dataclasses

host = '10.0.2.15'
port = 13117
ip_start = host[:host.rfind('.') + 1]

ip_range_list = ['{}{}'.format(ip_start, x) for x in range(0, 256)]

ip_range_list.append('25.45.173.121')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\u001b[31m'
    Magenta = '\u001b[35'
    Yellow = '\u001b[33'
    purple = '\033[35m'
    RESET = '\u001b[0m'
    BackgroundBrightMagenta = '\u001b[45;1m'
    BackgroundBrightCyan = '\u001b[46;1m'
    pink = '\033[91m'
    B_White = "\x1b[107m"
    darkgrey = '\033[90m'
    white= '\u001b[37m'


@dataclasses.dataclass
class Msg:
    Magic_cookie: bytes
    Message_type: bytes
    Server_port: bytes

    def get_port_as_bytes(self):
        return self.Server_port

    def get_Message_type(self):
        return self.Message_type

    def get_Magic_cookie(self):
        return self.Magic_cookie

    def msg_to_bytes(self):
        return self.Magic_cookie + self.Message_type + self.Server_port


def bytes_to_msg(bytes):
    msg_type = bytes[:4]
    msg_data = bytes[4]
    port = bytes[5:7]
    return msg_type.decode("utf-8"), msg_data.deocde("utf-8"), port.decode("utf-8")


frame = bytes([0xfe, 0xed, 0xbe, 0xef])
type = bytes([0x02])
s = struct.pack('>H', port)
Msgsend = Msg(frame, type, s).msg_to_bytes()
