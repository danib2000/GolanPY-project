import socket, Queue, time
from PIL import ImageGrab, Image
from io import BytesIO
from threading import Thread

KA_on = True
def recv_img(socket):
    file=open('img.jpg','wb')
    temp=socket.recv(1024)
    print "first temp length "+str(len(temp))
    while len(temp)==1024:
        file.write(temp)
        print len(temp)
        temp=socket.recv(1024)
    file.write(temp)
    file.close()
        
def select_command(sock):
    global KA_on
    print 'please select your desired command:'
    print 'press 1 for TIME'
    print 'press 2 for name'
    print 'press 3 to see directory'
    print 'press 4 to see screen shot'
    print 'press 5 to stop keep alive'
    print 'press 6 to exit'
    choice = raw_input()
    if choice == '1':
        get_time(sock)
    elif choice == '2':
        get_name(sock)
    elif choice == '3':
        get_dir(sock)
    elif choice == '4':
        get_img(sock)
    elif choice == '5':
        sock.send("STOP_KEEP_ALIVE")
        ka_on = False
    elif choice == '6':
        print 'closing connection'
        sock.close()
        
        
def get_time(sock):
    sock.send("TIME")
    data = sock.recv(1024)
    print data

def get_name(sock):
    sock.send("NAME")
    data = sock.recv(1024)
    print data

def get_dir(sock):
    path = raw_input("please enter the path of the directory you wish to see:")
    sock.send("SEE_DIR")
    sock.send(path)
    data = sock.recv(1024)
    print data

def get_img(sock):
    sock.send("SEE_SCREEN")
    recv_img(sock)

def log_in(sock):
    data = raw_input("press 1 to connect \n press 2 to register:")
    if data == '1':
        sock.send("connect")
        data = raw_input("please enter userName:")
        sock.send(data)
        data = raw_input("please enter password:")
        sock.send(data)
        data = sock.recv(1024)
        print data
    elif data == '2':
        sock.send("register")
        data = raw_input("please enter UserName:")
        sock.send(data)
        data = raw_input("please enter password:")
        sock.send(data)
        
def keep_alive(sock):
    keepAlive_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keepAlive_sock.connect(("127.0.0.1",4321))
    global KA_on
    while KA_on:
        data = keepAlive_sock.recv(1024)
        print data
        keepAlive_sock.send("IM ALIVE")
        time.sleep(9)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1",1234))
    log_in(s)
    keepAlive_t = Thread(target=keep_alive,args=(s,))   
    keepAlive_t.start()

    while True:
        select_command(s)
    s.close()
        

if __name__ == "__main__":
    main()
