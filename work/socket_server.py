import socket

# 用IPV4，和TCP协议
scok = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
scok.bind(('',8000))#绑定端口
print("this is socket_server:127.0.0.1:80000")
scok.listen(5)#监听
con,add = scok.accept()#阻塞
con.recv(512)
con.send("Hello i am your server")
scok.close()

