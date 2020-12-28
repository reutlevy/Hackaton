import selectors
import socket
import types
from threading import Thread
import time
from config import *
import random

team_map = {'group 1': [], 'group 2': []}
group1_ips = []
group2_ips = []
couter_group1 = 0
couter_group2 = 0

sel = selectors.DefaultSelector()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lsock:
    lsock.bind((host, port))
    lsock.listen()
    print(bcolors.BackgroundBrightMagenta + bcolors.BOLD + 'Server started, listening on IP address ', host, bcolors.RESET)
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)



    def accept_wrapper(sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(bcolors.RED + 'accepted connection from' + bcolors.RESET, addr)
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

    def client_to_team(key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024).decode("utf-8")  # Should be ready to read
            if recv_data:
                if (len(team_map.get('group 1')) < len(team_map.get('group 2'))):
                    team_map['group 1'].append((recv_data, key, mask))
                    group1_ips.append(data.addr[0])
                elif (len(team_map.get('group 2')) > len(team_map.get('group 1'))):
                    team_map['group 2'].append((recv_data, key, mask))
                    group2_ips.append(data.addr[0])
                else:
                    group, arr = random.choice(list(team_map.items()))
                    team_map[group].append((recv_data, key, mask))
                    if group == 'group 1':
                        group1_ips.append(data.addr[0])
                    else:
                        group2_ips.append(data.addr[0])
            else:
                try:
                    sel.unregister(sock)
                    sock.close()
                    print(bcolors.BackgroundBrightMagenta + bcolors.BOLD + 'closing connection to', data.addr)
                except:
                    pass

    def send_start_game(key, mask, group1, group2):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            data.outb += """Welcome to Keyboard Spamming Battle Royale.
                            Group 1:
                            ==
                            {}
                            Group 2:
                            ==
                            {}
                            Start pressing keys on your keyboard as fast as you can!!""".format(group1, group2) \
                .encode('ascii')
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                try:
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]
                except:
                    for conn in team_map.get('group 1'):
                        if conn[1] == key:
                            team_map.get('group 1').remove(conn)
                    for conn in team_map.get('group 2'):
                        if conn[1] == key:
                            team_map.get('group 2').remove(conn)
                    try:
                        sel.unregister(sock)
                        sock.close()
                        print(bcolors.BackgroundBrightMagenta + bcolors.BOLD + 'closing connection to', data.addr)
                    except:
                        pass

    def get_char_from_client(key, mask):
        global couter_group1
        global couter_group2
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                if (data.addr[0] in group1_ips):
                    couter_group1 = couter_group1 + 1
                elif (data.addr[0] in group2_ips):
                    couter_group2 = couter_group2 + 1
            else:
                try:
                    sel.unregister(sock)
                    sock.close()
                    print(bcolors.BackgroundBrightMagenta + bcolors.BOLD + 'closing connection to', data.addr)
                except:
                    pass
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]

    def send_game_over(key, mask, msg):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            data.outb += msg
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                try:
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]
                    try:
                        sel.unregister(sock)
                        sock.close()
                        print(bcolors.BackgroundBrightMagenta + bcolors.BOLD + 'closing connection to', data.addr)
                    except:
                        pass
                except:
                    try:
                        sel.unregister(sock)
                        sock.close()
                        print(bcolors.BackgroundBrightMagenta + bcolors.BOLD + 'closing connection to', data.addr)
                    except:
                        pass

    def send_udp_invaite():
        msg = Msgsend
        t_end = time.time() + 10
        while time.time() < t_end:
            for ip in ip_range_list:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    sock.sendto(msg, (ip, port))
                    sock.close()
                except:
                    pass



    def main():
        global group1_ips, group2_ips, team_map, couter_group1, couter_group2

        while True:
            t1 = Thread(name='udp', target=send_udp_invaite)
            t1.setDaemon(True)
            t1.start()
            t_end = time.time() + 10
            while time.time() < t_end:
                events = sel.select(timeout=(t_end - time.time()))
                for key, mask in events:
                    if key.data is None:
                        accept_wrapper(key.fileobj)
                    else:
                        client_to_team(key, mask)
            t1.join()
            print("group1= ", group1_ips)
            print("group2= ", group2_ips)

            group1 = ''.join([i[0] for i in team_map.get('group 1')])
            group2 = ''.join([i[0] for i in team_map.get('group 2')])
            for client in team_map.get('group 1'):
                send_start_game(client[1], client[2], group1, group2)
            for client in team_map.get('group 2'):
                send_start_game(client[1], client[2], group1, group2)

            t_end = time.time() + 10
            while time.time() < t_end:
                events = sel.select(timeout=(t_end - time.time()))
                for key, mask in events:
                    if key.data is None:
                        accept_wrapper(key.fileobj)
                    else:
                        get_char_from_client(key, mask)
            if (couter_group1>couter_group2):
                winner_group ="Group 1"
                winner_group_teams =group1
            else:
                winner_group = "Group 2"
                winner_group_teams = group2
            winner_msg = """Game over!
                            Group 1 typed in {} characters. Group 2 typed in {} characters.
                            {} wins!
                            
                            Congratulations to the winners:
                            ==
                            {}""".format(couter_group1,couter_group2,winner_group, winner_group_teams) \
                    .encode('ascii')

            for client in team_map.get('group 1'):
                send_game_over(client[1], client[2], winner_msg)
            for client in team_map.get('group 2'):
                send_game_over(client[1], client[2], winner_msg)

            team_map = {'group 1': [], 'group 2': []}
            group1_ips = []
            group2_ips = []
            couter_group1 = 0
            couter_group2 = 0
            print(bcolors.OKCYAN+"“Game over, sending out offer requests...")





    main()
