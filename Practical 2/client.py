import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socket.gethostname(),1234))

while True: #recieve the data
    msg = sock.recv(1024) #buffering 8 is the number of 
    print("Mesage Recieved : ")
    print(msg.decode("utf-8"))

