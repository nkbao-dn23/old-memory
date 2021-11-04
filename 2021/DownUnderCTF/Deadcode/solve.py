from pwn import *

r = remote("wn-2021.duc.tf", 31916)
r.recv()

flag = 