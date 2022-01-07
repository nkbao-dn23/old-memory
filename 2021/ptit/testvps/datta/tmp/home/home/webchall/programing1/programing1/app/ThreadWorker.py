
from threading import Thread
import random
from socket import timeout

try:
    flag  = open('/flag','r').read() 
except:
    flag = "None"    



def newCal():
    mode = '+-*/'
    a = 10
    b = 100000
    numberCal = random.randint(2,8)

    s = f"{random.randint(a,b)} "

    for _ in range(numberCal):
        s += f" {random.choice(mode)} {random.randint(a,b)}"

    return s,eval(s.replace('/','//'))

class worker(Thread):
    def __init__(self, con) -> None:
        super(worker,self).__init__()
        self.con = con

    def run(self) -> None:
        self.con.send(b"Say hi!!\n\nWelcome to ChirstCTF. In order to get flag, you must answer all my questions.\n\n")
        for i in range(0,789*2,1):
            cal, result = newCal()

            self.con.send(("Number %s.\n\n%s = ?\n\n"%(i+1,cal)).encode())
            try:
                answer = self.con.recv(4096).decode()
            except timeout as e:
                self.con.send(b'Timeout\n')
                self.con.close()  
                return

            try:
                answer = int(answer)
                if answer != result:
                    self.con.send(b'Wrong\n\n')
                    self.con.close()
                    return
                else:
                    self.con.send(b'Correct!\n\n')    
            except:
                self.con.send(b'Give me a number\n\n')
                self.con.close()
                return
        self.con.send(("\n\nFlag: %s \n\n"%flag))    
        self.con.close()