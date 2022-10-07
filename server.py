import socket
import json

UDP_IP = "192.168.42.174"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

users = {}

while True:
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    request = json.loads(data)
    if request["type"] == "login":
        print(1)
        if request["nickname"] not in users.values():
            users[addr] = request["nickname"]
            ans = {"type": "status", "error": "", "status": "ok"}
            print(f"User {request['nickname']} successful connected")
            sock.sendto(bytes(json.dumps(ans), 'utf-8'), addr)
        else:
            users[addr] = request["nickname"]
            ans = {"type": "status", "error": "User already login", "status": "error"}
            print(f"User {request['nickname']} error on connection")
            sock.sendto(bytes(json.dumps(ans), 'utf-8'), addr)
    elif request["type"] == "message":
        print(2)
        message = {"type": "message", "text": f"{users[addr]}: {request['text']}"}
        for add in users.keys():
            if addr != add:
                sock.sendto(bytes(json.dumps(message), 'utf-8'), add)

