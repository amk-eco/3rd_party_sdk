import sys
import socket

HOST='127.0.0.1'
PORT=50123 #서버와 같은 포트사용

# print(len(sys.argv))
string=''
for i in range(1,len(sys.argv)):
    string +=sys.argv[i]+" "
    print(string)

string = string[:-1]
string.strip()    

client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

client_socket.send(string.encode())
data=client_socket.recv(1024)
print("Received ", repr(data))
# if data.decode('utf-8') =='quit':
    # break

