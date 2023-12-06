import socket
from _thread import *
import sys
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
server = ip_address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]),int(str[2]), int(str[3]), int(str[4])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + ',' + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4])

pos = [(100,250,0,0,250),(400,250,100,100,250)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0


## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")
ip_int = ip_address.split(".")

join_code = []
for x in range(0,4):
    y = 0
    y2 = int(ip_int[x])%16
    y = (int(ip_int[x])-y2)/16
    join_code.append(y)
    join_code.append(y2)


for x in range(0,len(join_code)):
        join_code[x] = int(join_code[x])

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
for x in range(0,len(join_code)):
        join_code[x] = alphabet[join_code[x]]

print(join_code)
    
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1