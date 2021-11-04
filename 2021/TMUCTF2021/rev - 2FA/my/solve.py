from pwn import *
r = remote("194.5.207.190", 6030)
r = process("./2fa")
gdb.attach(r)


r.recvuntil(b'>')
r.sendline(b"G7yTu83M")
r.recvuntil(b'password')
r.sendline(b'50_57R0nG_P455w02d_83467')
print(r.recvuntil(b'flag ===>>>'))
payload = b'ab'
r.sendline(payload)

r.interactive()