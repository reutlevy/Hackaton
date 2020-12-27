import operator
import socket
import time

from pip._vendor.msgpack.fallback import xrange

from config import *
from pynput.keyboard import Key, Listener

s = None
t_end = time.time()

a_dict = {}


def on_press(key):
    if time.time() > t_end:
        return False
    s.sendall(b'char')
    if key in a_dict:
        a_dict["c"] += 1
    else:
        a_dict["c"] = 1


while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", port))
    # while True:
    # Thanks @seym45 for a fix
    print(bcolors.BOLD + bcolors.purple + "Client started, listening for offer requests..." + bcolors.RESET)
    data, addr = client.recvfrom(1024)
    if not (data[:4] == bytes([0xfe, 0xed, 0xbe, 0xef])) or not (data[4] == 0x02):
        print("not the correct format")
    else:
        host = addr[0]
        print(bcolors.OKCYAN + "Received offer from {}, attempting to connect...".format(host))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port_new = struct.unpack('>H', data[5:7])[0]
            s.connect((host, port_new))
            s.sendall(b'client team name\n')
            data = s.recv(1024)
            print(bcolors.RED)
            print(data.decode("utf-8"))
            t_end = time.time() + 10
            with Listener(
                    on_press=on_press) as listener:
                listener.join()

            maximum = max(a_dict, key=a_dict.get)
            print('\n')
            print(bcolors.OKBLUE+bcolors.BOLD+"The most typed char is", maximum)
            print(bcolors.Yellow + 'Received', repr(data))
            print(bcolors.purple + "end")
            s = None
            t_end = time.time()
