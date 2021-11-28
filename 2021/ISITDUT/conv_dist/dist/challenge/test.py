from pwn import *

for _ in range(1):
	r = process("./challenge")
	gdb.attach(r)
	r.recvuntil(b'>')
	
	def func1(size, name):
		r.sendline(b'1')
		r.recvuntil(b'String length:')
		r.sendline(str(size).encode("utf-8"))
		r.recvuntil(b'String:')
		r.send(name)
		return r.recvuntil(b'>')
	
	def func2(size, name):
		r.sendline(b'2')
		r.recvuntil(b'(in bytes):')
		r.sendline(str(size).encode("utf-8"))
		r.recvuntil(b'String:')
		r.send(name)
		return r.recvuntil(b'>')
	
	def func3(size):
		r.sendline(b'3')
		r.recvuntil(b'String length:')
		r.sendline(str(size).encode("utf-8"))
		r.recv()
		return r.recvuntil(b'>')
	
	
	size = 12
	payload = b'a'*size*4 
	stuff = func1(size, payload)
	
	r.interactive()