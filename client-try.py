import socket
from config import *
from threading import Thread
import getch

s = None
can_send = False

def start_listener():
    while 1:
        if can_send:
            ch = getch.getch()
            if ord(ch) == 3 or ord(ch) == 4:
                break

            if can_send:
                s.sendall(str(ch).encode('utf-8'))


t1 = Thread(name='listener', target=start_listener)
t1.setDaemon(True)
t1.start()

print(bcolors.BOLD + bcolors.purple + "Client started, listening for offer requests..." + bcolors.RESET)

while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", port))
    data, addr = client.recvfrom(1024)
    if not (data[:4] == bytes([0xfe, 0xed, 0xbe, 0xef])) or not (data[4] == 0x02):
        print("not the correct format")
    else:
        host = addr[0]
        print(bcolors.OKCYAN + "Received offer from {}, attempting to connect...".format(host))


        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            port_new = struct.unpack('>H', data[5:7])[0]
            s.connect((host, port_new))
            s.sendall(b'Maor Golesh\n')
            start_game_msg = s.recv(1024).decode("utf-8")
            print(start_game_msg)
            can_send = True
            end_game_msg = s.recv(1024).decode("utf-8")
            can_send = False

            print(bcolors.white + end_game_msg)
            print(
                bcolors.BOLD + bcolors.purple + "Server disconnected, listening for offer requests..." + bcolors.RESET)
            s = None
