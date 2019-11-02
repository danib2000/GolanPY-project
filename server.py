#server
import socket, os, time
from threading import Thread, Lock
from PIL import ImageGrab, Image
from io import BytesIO

socket_list=[]
addr_list=[]
sock_threads = []
mutex = Lock()
keepAlive_threads = []
keepAlive_sockets = []
keepAlive_addrs = []
KAis_on = True
def sock_connet(socket):
    global socket_list
    global addr_list
    global threads
    while True:
        print 'wait for connection'
        conn,addr=socket.accept()
        socket_list.append(conn)
        addr_list.append(addr)
        #log_in(conn)
        if log_in(conn) == True:
            sock_t = Thread(target=Wait_For_Command,args=(conn,))
            sock_threads.append(sock_t)   
            sock_t.start()



def keep_alive(is_on, index):
    keepAlive_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    keepAlive_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    keepAlive_sock.bind(("0.0.0.0",4321))
    keepAlive_sock.listen(1)
    conn,addr = keepAlive_sock.accept()
    global KAis_on
    global socket_list
    while KAis_on:
        conn.send("is connected?")
        conn.settimeout(10)
        try:
            rec = conn.recv(1024) 
            print rec
        except socket.timeout: # fail after 10 second of no activity
            print("not alive :( [Timeout]")
            KAis_on = False
    keepAlive_sock.close()
    conn.close()
    socket_list[index].close()
            

def file_is_empty(path):
    return os.stat(path).st_size==0

def Wait_For_Command(sock):
    '''waits for a command from Csock, then does what the command asked for'''
    global KAis_on
    global socket_list
    is_on = True
    global keepAlive_threads
    keepAlive_t = Thread(target=keep_alive,args=((is_on, len(socket_list)-1)))
    keepAlive_threads.append(keepAlive_t)   
    keepAlive_t.start()
    while is_on: 
        choice=""
        choice=sock.recv(1024)
        print choice
        if "TIME" in choice:
            get_time(sock)
        elif choice=="NAME":
            get_name(sock)
        elif "START_APP" in choice:
            start_app(sock)
        elif "SEE_SCREEN" in choice:
            send_screen_shot(sock)
        elif "SEE_DIR" in choice:
            send_dir(sock)
        elif "STOP_KEEP_ALIVE" in choice:
            KAis_on = False
        elif choice=="EXIT":
            sock.close()
            is_on = False
            sys.exit(0)

def start_app(sock):
    path = sock.recv(1024)
    try:
        os.startfile(path)
    except:
        sock.send("Invalid path")

def get_time(sock):
    '''sends the current time'''
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    sock.send("TIME IS:" + current_time)

def get_name(sock):
    '''sends the name of os computer name'''
    name = socket.gethostname()
    sock.send("THE NAME IS:" + name)

def send_screen_shot(sock):
    '''sends the screen shot at 2048 bytes a time'''
    img = screen_shot()
    POI = img.read(2048)
    while len(POI)==2048:
        sock.send(POI)
        POI=img.read(2048)
    sock.send(POI)

def compress(image):
    ''' compresses the screen shot'''
    file=BytesIO()
    image.save(file, 'jpeg', quality=60)
    file.name='t.jpg'
    file.seek(0)
    return file

def screen_shot():
    ''' takes a screen shot'''
    img=ImageGrab.grab()
    img=compress(img)
    return img

def send_dir(sock):
    ''' sends all the files in the directory'''
    path = sock.recv(1024)
    try:
        file_list = os.listdir(path)
        files = ", ".join(file_list)
        sock.send("Files in directory are:" + files)
    except:
        sock.send("Invalid path")

        
def create_new_user(f, sock):
    global mutex
    mutex.acquire()
    user = sock.recv(1024)
    password = sock.recv(1024)
    f.write(user + " " + password + "\r\n")
    mutex.release()

def check_log_in(f, userName, password):
    f1 = f.readlines()    
    for line in f1:
        print(line)
        if userName in line and password in line:
            return True
    return False


def log_in(sock):
    name = "users.txt" 
    f = open(name, "a+")
    data = sock.recv(1024)
    if data == "connect":
        user = sock.recv(1024)
        password = sock.recv(1024)
        b = check_log_in(f, user, password)
        if b == False:
            sock.send("bad connection parameters")      
            sock.close()
            return False
        else:
            sock.send("Connection successful")
            return True
    elif data == "register":
        print 'b'
        create_new_user(f, sock)


def main():
    global socket_list
    global addr_list
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s1.bind(("0.0.0.0",1234))
    s1.listen(1)
    SocketConnThread=Thread(target=sock_connet,args=(s1,))
    SocketConnThread.start()





if __name__ == "__main__":
    main()


