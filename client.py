import socket
import time
from config import *
from pynput.keyboard import Key, Listener

s = None
t_end = time.time()

a_dict = {}


def on_press(key):
    # if time.time() > t_end:
    #     return False
    s.sendall(str(key).encode('ascii'))
    if key in a_dict:
        a_dict[str(key)] = a_dict[str(key)] + 1
    else:
        a_dict[str(key)] = 1

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
            s.sendall(b'Rubins\n')
            start_game_msg = s.recv(1024).decode("utf-8")
            print(bcolors.RED)
            print(start_game_msg)
            t_end = time.time() + 10
            with Listener(
                    on_press=on_press,timeout=10) as listener:
                # listener.start()
                # time.sleep(10)
                end_game_msg = s.recv(1024).decode("utf-8")
                listener.stop()

            print(bcolors.RED)
            print(end_game_msg)
            print(bcolors.BOLD + bcolors.purple + "Server disconnected, listening for offer requests..." + bcolors.RESET)
            s = None
            t_end = time.time()


            # try:
            #     maximum = max(a_dict, key=a_dict.get)
            # except:
            #     maximum = "not prass on any char"
            #
            # print(a_dict)
            # print('\n')
            # print(bcolors.OKBLUE+bcolors.BOLD+"The most typed char is", maximum)
            # print(bcolors.Yellow + 'Received', repr(data))

