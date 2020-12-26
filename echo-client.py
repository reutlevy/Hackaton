import socket
import time

from config import *
from pynput.keyboard import Key, Listener

s = None
t_end = time.time()
def on_press(key):
    if time.time() > t_end:
        return False
    s.sendall(b'char')
    print('{0} pressed'.format(
        key))

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", port))
# while True:
# Thanks @seym45 for a fix
print("Client started, listening for offer requests...")
data, addr = client.recvfrom(1024)
print(data.decode('utf-8'))
print(data.decode('utf-8')[:10])
print(data.decode('utf-8')[10:14])

if (not (data.decode('utf-8')[:10]==0xfeedbeef)) or (not data.decode('utf-8')[11:14]==0x02):
    print("not the correct format")
host = addr[0]
print("Received offer from {}, attempting to connect...".format(host))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b'client team name\n')
    data = s.recv(1024)
    print(data.decode("utf-8"))
    t_end = time.time() + 10
    with Listener(
            on_press=on_press) as listener:
        listener.join()

    print('Received', repr(data))
    print("end")

