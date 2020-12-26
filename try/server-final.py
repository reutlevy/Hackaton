import socket
from time import sleep
import os, re
from config import *


def main():
    number = 1
    while True:

        for ip in ip_range_list:
            print(f'\u001b[3{number};1m' + f'sending on {ip}' + bcolors.RESET)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # sock.bind((ip,0))
            frame = bytes([0xfe,0xed,0xbe,0xef])
            type= bytes([0x02])
            Msgsend=Msg(frame, type, bytes(port))
            sock.sendto(Msgsend.msg_to_bytes(), (ip, port))
            sock.close()
            if number == 7:
                number = 1
            else:
                number += 1

        sleep(2)


main()
