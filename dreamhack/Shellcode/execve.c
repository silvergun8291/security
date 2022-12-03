__asm__(
    ".global run_sh\n"
    "run_sh:\n"
    
    "mov rax, 0x68732f6e69622f	# rax = '/bin/sh'\n"
    "push rax			# '/bin/sh' 스택에 넣기\n"
    "mov rdi, rsp		# rdi = '/bin/sh'\n"
    "xor rsi, rsi		# rsi = 0x0 (null)\n"
    "xor rdx, rdx		# rdx = 0x0 (null)\n"
    "mov rax, 0x3b		# rax = 0x3b (execve)\n"
    "syscall			# execve('/bin/sh', null, null)\n"
    
    "xor rdi, rdi   		# rdi = 0\n"
    "mov rax, 0x3c		# rax = sys_exit\n"
    "syscall        		# exit(0)");
    
void run_sh();

int main() { run_sh(); }
