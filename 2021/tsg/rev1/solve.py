from pwn import *

database = ""

for i in range(0x30, 0x7e):
	database += chr(i)

flag = ""

for i in range(32):
	tmp = flag
	for j in database:
		tmp += j
		tmp += "+"*(32 - len(tmp))
		payload = "./beginners_rev " + tmp
		r = process(payload, shell=True)
		
		stuff = r.recvall()

		if( stuff.count(b"correct") > len(flag) ):
			flag += tmp
			break
		else:
			tmp = tmp[:-1]
print(flag)