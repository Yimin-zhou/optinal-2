import socket, sys, os, threading
from time import sleep

# if IN-USE restart
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def send(sock,ip,port):
    try:
        while True:
            # send msgs
            msg = input('You> ')

            if not msg:
                print('can not send empty msg')
                continue
            else:
                 # when user enter !who
                if msg == "!who":
                    loggedInUsers = "WHO\n".encode("utf-8")
                    sock.sendto(loggedInUsers,(ip,port))

                # quit client
                elif msg == "!quit":
                    sock.close()
                    exit()

                # slice the msg string
                elif msg.startswith("@"):
                    user = msg[1:msg.index(' ')]
                    myMsg = msg[msg.index(' '):]
                    sendUser = user.encode("utf-8")
                    sendMsg = myMsg.encode("utf-8")
                    send = "SEND ".encode("utf-8")
                    newLine = "\n".encode("utf-8")
                    sock.sendto((send + sendUser + sendMsg + newLine),(ip,port))

                else:
                    myMsg = msg.encode("utf-8")
                    newLine = "\n".encode("utf-8")
                    sock.sendto((myMsg+newLine),(ip,port))
                
            sleep(1)

        sock.close()

    except OSError as errorMsg1:
        print(errorMsg1)

def rec(sock,ip,port):
    try:
        while True:
            data,addr = sock.recvfrom(1024)

            print(data)

        sock.close()
    except OSError as errorMsg2:
        print(errorMsg2)


if __name__ == '__main__':

    UDP_IP = "18.195.107.195"
    UDP_PORT = 5382
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
            # first hand shake
            userName = input('Enter your username to start: ')
            name = userName.encode("utf-8")
            newLine = "\n".encode("utf-8")
            firstHandShake = "HELLO-FROM ".encode("utf-8")
            # sendall calls send repeatedly until all bytes are sent.
            sock.sendto((firstHandShake + name + newLine), (UDP_IP,UDP_PORT))

            # second handshake
            secondHandShake, addr = sock.recvfrom(4096)
            mySecondHandShake = secondHandShake.decode("utf-8")
            # check IN-USE
            if "IN-USE" in mySecondHandShake:
                print('Name has been taken, start over again')
                sock.close()
                restart()

            else:
                print (mySecondHandShake)

    except OSError as errorMsg:
        print(errorMsg)

    t1 = threading.Thread(target=send, args=(sock,UDP_IP,UDP_PORT))
    t2 = threading.Thread(target=rec, args=(sock,UDP_IP,UDP_PORT))
    t1.start()
    t2.start()
    t1.join()
    t2.join()