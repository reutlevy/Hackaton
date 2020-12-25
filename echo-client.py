import socket
import time

from config import *
from pynput.keyboard import Key, Listener

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

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", port))
# while True:
# Thanks @seym45 for a fix
print(bcolors.BOLD+bcolors.OKBLUE+"Client started, listening for offer requests...")
data, addr = client.recvfrom(1024)

print(addr)
# print("received message: %s"%data)
host = addr[0]
print(bcolors.BOLD+bcolors.OKCYAN+"Received offer from {}, attempting to connect...".format(host))

s = None
t_end = time.time()
def on_press(key):
    if time.time() > t_end:
        return False
    s.sendall(b'char')
    print('{0} pressed'.format(
        key))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b'reut\n')
    data = s.recv(1024)
    print(data.decode("utf-8"))
    t_end = time.time() + 10
    with Listener(
            on_press=on_press) as listener:
        listener.join()

    print('Received', repr(data))
    print("end")