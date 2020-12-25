import socket
from time import sleep
import os, re
from config import *

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
    RED= '\u001b[31m'
    Magenta= '\u001b[35'
    Yellow= '\u001b[33'

def main():

    msg = b'hello world'
    while True:

        for ip in ip_range_list:
            print(bcolors.OKGREEN+f'sending on {ip}')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # sock.bind((ip,0))
            sock.sendto(msg, (ip, port))
            sock.close()

        sleep(2)


main()

