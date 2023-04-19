.globl _start
.section .text
_start:
    xor %rax, %rax
    pushq %rax
    // %rdi - path, %rsi and %rdx - set to empty string
    movq %rsp, %rsi
    movq %rsp, %rdx


    movq $0x68732F6E69622F3b, %rbx
    mov %bl, %al

    // "/bin/sh 0x2F62696E2F7368
    // needs to change to little endianess
    pushq %rbx
    movq %rsp, %rdi
    inc %rdi

    syscall
