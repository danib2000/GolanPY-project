#server
import socket, os, time
from threading import Thread
from PIL import ImageGrab, Image

socket_list=[]
addr_list=[]

def sock_connet(socket):
    global socket_list
    global addr_list
    while True:
        print 'wait for connection'
        conn,addr=socket.accept()
        socket_list.append(conn)
        addr_list.append(addr)

def file_is_empty(path):
    return os.stat(path).st_size==0

def Wait_For_Command(sock):
    '''waits for a command from Csock, then does what the command asked for'''
    choice=""
    choice=sock.recv(1024)
    print choice
    if "TIME" in choice:
        get_time(sock)
    elif choice=="NAME":
        get_name(sock)
    elif "START_APP" in choice:
        #TODO add a start app function
    elif "SEE_SCREEN" in choice:
        send_screen_shot(sock)
    elif "SEE_DIR" in choice:
        send_dir(sock)
    elif "STOP_KEEP_ALIVE" in choice:
        #TODO add a keep alive function
    elif choice=="EXIT":
        Close()
        sock.close()
        sys.exit(0)

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
    POI=img.read(2048)
    while len(POI)==2048:
        socket.send(POI)
        POI=img.read(2048)
    socket.send(POI)

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

        
def create_new_user(conn):
    print 'a'

def log_in(conn):
    name = "pass.txt" 
    f = open(name, "w+")
    data = conn.recv(1024)
    if data == "connect" and !file_is_empty:
        conn.send("please enter your userName:")
        user = conn.recv(1024)
        conn.send("please enter your password:")
        password = conn.recv(1024)
        #TODO check if user and pass correct in file
    else
        create_new_user()


def main():
    global socket_list
    global addr_list
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s1.bind(("0.0.0.0",1234))
    s1.listen(1)
    conn, addr = s.accept()
    SocketThread=Thread(target=sock_connet,args=(s1,))
    SocketThread.start()




if __name__ == "__main__":
    main()


