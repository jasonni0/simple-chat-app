import socket, threading


def main():
    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print("\n************************************************************")
    print("***                 Simple Chatting APP 1.0.0            ***")
    print(f"***                {clientSocket.recv(1024).decode('utf-8')}               ***")
    print("***   Send your message in format '#clientID:message'    ***")
    print("***   Send '/getlist' to update available client list    ***")
    print("***   Send '/getblocklist' to see blocklist              ***")
    print("***   Send '/block clientID' to block a client           ***")
    print("***   Send '/unblock clientID' to unblock a client       ***")
    print("***   Send '.exit' to disconnect from server             ***")
    print("************************************************************")
    print(f"{clientSocket.recv(1024).decode('utf-8')}")

    def send():
        """send message"""
        while 1:
            send_msg = input("")
            clientSocket.send(send_msg.encode('utf-8'))
            if send_msg == '.exit':
                break

    def receive():
        """receive message"""
        while 1:
            recv_msg = clientSocket.recv(1024).decode('utf-8')
            if recv_msg == '.exit' or len(recv_msg) == 0:
                print('Disconnected from Server')
                break
            print(recv_msg)

    s = threading.Thread(target=send)
    r = threading.Thread(target=receive)
    s.start()
    r.start()
    s.join()
    r.join()


if __name__ == "__main__":
    main()
