import socket, string, random, threading, time
from datetime import datetime


def get_time():
    """get current time"""
    return str(datetime.now().hour) + ':' + str(datetime.now().minute)


def id_generator():
    """Generate an ID"""
    number = str(random.randint(0, 9))
    l = [random.choice(string.ascii_lowercase) for _ in range(4)]
    s = ''.join(l)
    return number + s


def get_id(clients):
    """get a unique id"""
    id_num = id_generator()
    while id_num in clients:
        id_num = id_generator()
    return id_num


def get_clients(clients, id_num):
    """Update client list"""
    available_clients = list(clients.keys())
    available_clients.remove(id_num)
    return available_clients


def create_client(connectionSocket, id_num, clients, available_clients, blocklist):
    """Manage client's behavior"""
    while 1:
        msg = connectionSocket.recv(1024).decode()
        if msg[:8] == '/unblock' and msg[9:] in clients and msg[9:] != id_num and msg[9:] in blocklist[id_num]:
            blocklist[id_num].remove(msg[9:])
            continue
        if msg[:6] == '/block' and msg[7:] in clients and msg[7:] != id_num and msg[7:] not in blocklist[id_num]:
            blocklist[id_num].append(msg[7:])
            continue
        if msg == '/getlist':
            available_clients = get_clients(clients, id_num)
            connectionSocket.send((f"{get_time()} Available Clients:{str(available_clients)}").encode('utf-8'))
            continue
        if msg == '/getblocklist':
            connectionSocket.send((f"{get_time()} Blocklist:{blocklist[id_num]}").encode('utf-8'))
            continue
        if msg == '.exit' or len(msg) == 0:
            connectionSocket.send(".exit".encode('utf-8'))
            del blocklist[id_num]
            del clients[id_num]
            print(f"{get_time()} Client {id_num} Disconnected")
            break
        try:
            if msg[0] == '#' and msg[1:msg.index(':')] == id_num:
                connectionSocket.send((f"{get_time()} Error: You cannot send the message to yourself").encode('utf-8'))
            elif msg[0] == '#' and msg[1:msg.index(':')] not in clients:
                connectionSocket.send((f"{get_time()} Error: Client ID not found").encode('utf-8'))
            elif msg[:6] == '/block' and msg[7:] == id_num:
                connectionSocket.send((f"{get_time()} Error: You cannot block yourself").encode('utf-8'))
            elif msg[:6] == '/block' and msg[7:] not in clients:
                connectionSocket.send((f"{get_time()} Error: Client ID not found").encode('utf-8'))
            elif msg[:6] == '/block' and msg[7:] in blocklist[id_num]:
                connectionSocket.send((f"{get_time()} Error: Already blocked client {msg[7:]}").encode('utf-8'))
            elif msg[:8] == '/unblock' and msg[9:] == id_num:
                connectionSocket.send((f"{get_time()} Error: You cannot unblock yourself").encode('utf-8'))
            elif msg[:8] == '/unblock' and msg[9:] not in blocklist[id_num]:
                connectionSocket.send((f"{get_time()} Error: Client ID not found").encode('utf-8'))
            elif id_num in blocklist[msg[1:msg.index(':')]]:
                connectionSocket.send((f"{get_time()} Error: Client {msg[1:msg.index(':')]} blocked you").encode('utf-8'))
            else:
                clients[msg[1:msg.index(':')]].send((f"{get_time()} From {id_num}:{msg[msg.index(':')+1:]}").encode('utf-8'))
        except:
            connectionSocket.send((f"{get_time()} Error: Incorrect Format, Please Read Description Again").encode('utf-8'))
    connectionSocket.close()


def main():
    clients = {}
    blocklist = {}
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverPort = 12000
    serverSocket.bind(('', serverPort))
    serverSocket.listen()
    print(f"{get_time()} The server is started")
    while 1:
        id_num = get_id(clients)
        connectionSocket, _ = serverSocket.accept()
        clients[id_num] = connectionSocket
        blocklist[id_num] = []
        available_clients = get_clients(clients, id_num)
        print(f"{get_time()} Client {id_num} Connected")
        connectionSocket.send((f"Your Client ID is {id_num}").encode('utf-8'))
        time.sleep(1)
        connectionSocket.send((f"\n{get_time()} Available Clients:{str(available_clients)}").encode('utf-8'))
        threading._start_new_thread(create_client, (connectionSocket, id_num, clients, available_clients, blocklist))
    connectionSocket.close()


if __name__ == "__main__":
    main()