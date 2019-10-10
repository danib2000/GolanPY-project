#server
import socket
import os

def file_is_empty(path):
    return os.stat(path).st_size==0

def listen_for_command(conn):
    print 'a'
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
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    addr=('127.0.0.1',5556)
    sock.bind(addr)
    sock.listen(1)
    conn, addr = s.accept()





if __name__ == "__main__":
    main()


