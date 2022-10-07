import socket
import json
from time import time

import select

UDP_IP = "85.193.92.74"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

login_data = {"type": "login",
              "nickname": input('Your nickname: ')}
timee = time()
sock.sendto(bytes(json.dumps(login_data), 'utf-8'), (UDP_IP, UDP_PORT))
print(0)
data, addr = sock.recvfrom(1024)
print(1)
request = json.loads(data)
print(2)
if request["status"] != "ok":
    print(3)
    print(request["error"])
    input()
    quit(1)
else:
    print(4)
    print("Successful connection in", time() - timee)

while True:
    message = {"type": "message", "text": input('Message: ')}
    sock.sendto(bytes(json.dumps(message), 'utf-8'), (UDP_IP, UDP_PORT))
    have_data = True
    while have_data:
        timeout = 0.1  # wait in seconds
        ready_sockets, _, _ = select.select(
            [sock], [], [], timeout
        )
        if ready_sockets:  # work max 0.1 sec
            data = sock.recv(1024)
            print(data)
        else:  # if work more
            have_data = False
