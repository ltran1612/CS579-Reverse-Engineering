.globl _start
.section .text
_start:
    xor %rax, %rax
    pushq %rax
    mov $0x3b, %eax
    // %rdi - path, %rsi and %rdx - set to empty string
    movq %rsp, %rsi
    movq %rsp, %rdx

    // "/bin/sh 0x2F62696E2F7368
    // needs to change to little endianess
    movq $0x68732F6E69622F, %rdi
    pushq %rdi
    movq %rsp, %rdi
    syscall
