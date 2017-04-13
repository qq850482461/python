import socket
scok = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("this is scoket_client")
scok.connect(("127.0.0.1",8000))#连接服务器
scok.send("Hello i am your client")
scok.close()