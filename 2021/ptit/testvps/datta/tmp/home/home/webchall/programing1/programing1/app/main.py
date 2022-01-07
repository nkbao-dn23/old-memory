import socket, os
from ThreadWorker import worker

s = socket.socket()
port = os.getenv("PORT") or 8888
s.bind(('',int(port)))
s.listen(5)           

while True:
    c, addr = s.accept()    
    c.settimeout(2)
    
    print ('Got connection from', addr )
    newWorker = worker(c)
    newWorker.start()
