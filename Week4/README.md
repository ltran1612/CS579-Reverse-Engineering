# Week 4

In week 4, we reviewed about assembly language and went through in particular the x86 instruction set. 
We then learned how to use Ghidra to reverse a test program called keyg3nme, used to check license key, to find out what are the possible license keys.  

## Ghidra Lab

### Executive Summary

The license key is an integer that is a multiple of 1223.

This program reads in an integer from STDIN. 

Then, it checks if the read integer is a license key. 
  
  - If so, it prints out: "Good job mate, now go keygen me.". 

  - Else it print: "nope.".

### Evidence

I analyzed keyg3nme program using Ghidra CodeBrowser. 

The first thing I did was checking the main function. In main, I found: 

1) __isoc99_scanf(&DAT_0010201a,&local_14: 
    - This is very likely scanf of C because it has scanf in its name. 
    - DAT_0010201a: This is the string"%d", so scanf is reading in an integer and put it in &local_14. 
    - I renamed &local_14 to input_num.

2) local_10 = *(long *)(in_FS_OFFSET + 0x28);:
    - 0x28 = 40 in decimal. 
    - *(long *)(in_FS_OFFSET + 0x28) gives us the value at the address of in_FS_OFFSET + 40.
    - By clicking on the line of code, I found that this line corresponds to the assembly "MOV RAX,qword ptr FS:[0x28]". 

      Googling showed that FS:[0x28] access the stack guard to check if the stack frame is corrupted. This seemd to be just a default functions put in and does not hold any functions regarding key checking. 

    - I renamed local_10 to stack_guard_value. 

3) After reading the input with scanf, main called validate_key(input_num)
    - Function prototype of validate_key(): bool validate_key(int). 
    
      I found it by clicking on the decompiled version of validate_key. 
    - This function returns 1 (True) if the input modulo with 0x4c7 (1223 in decimal) equals to 0, else 0 (False). 
    - From the name, this function is used to validate the key for license. So, the equation for the key is:

          key % 1223 = 0 
          => key = 1223 * c (where c is any integer). 
        
        In other words, the license key is an integer that is a multiple of 1223. 

4) The return value of validate_key() is then stored in a variable and used in an if statement:
    - I renamed that variable to key_similar_to_1223. 
    - In the if statement, if key_similar_to_1223 is 1 (True) then, we print out "Good job mate, now go keygen me.". Else we print "nope.".

**Main Function Modified After the Analysis:**

      undefined8 main(void)

      {
        int key_similar_to_1223;
        long in_FS_OFFSET;
        undefined4 input_num;
        long stack_guard_value;
        
        stack_guard_value = *(long *)(in_FS_OFFSET + 0x28);
        printf("Enter your key:  ");
        scanf(&DAT_0010201a,&input_num);
        key_similar_to_1223 = validate_key(input_num);
        if (key_similar_to_1223 == 1) {
          puts("Good job mate, now go keygen me.");
        }
        else {
          puts("nope.");
        }
        if (stack_guard_value != *(long *)(in_FS_OFFSET + 0x28)) {
                          /* WARNING: Subroutine does not return */
          __stack_chk_fail();
        }
        return 0;
      }

The general execution steps of this program is: 
1) Read in an integer.
2) Use validate_key() to check if the read integer is a key. 
    
    - If yes: print "Good job mate, now go keygen me.".
    - if no: print "nope.".
3) Exit

We ignore the operations relating to stack_guard_value because it seems to be default codes from the C compiler to check for memory corruption and are not related to the main function of the program. 

**Validate Key Function Declaration:**

    bool validate_key(int param_1)

    {
      return param_1 % 0x4c7 == 0;
    }

## Questions and Answeres

#### What is the difference between machine code and assembly?

Machine codes are the codes that the CPU can understand directly.

They are in the form of a binary string of certain length.

These binary strings are divided into multiple smaller sections (each section will have a set of possible values): 

- opcodes: To identify which type of instruction it is. For example, an instruction to add numbers, or to read from memory. 

- operands: To identify what the instruction does exactly. For example, with the add instruction, the operands are the 2 registers/numbers to add, and the address/register to store them. Another example is with the read from memory, the operand would be the address to read from and the register to store the read value.  

However, these codes are hard to read and write since we humans don't read in 0s and 1s. 

Thus, assembly language replaces the opcodes and the operands with easy-to-read for humans alternatives. For example, the opcode for read from memory could be "READ" instead of some order of 0s and 1s. There could also be some shorcut sytax to make it easier to write codes.

However, there is always a direct translation from a line of assembly to an equivalent same line of machine code.  

As a result, the difference between machine code and assembly code is that the components of each line of code in the machine code is in 0s and 1s, while those of assembly codes are in a human-readable format. 

#### If the ESP register is pointing to memory address 0x001270A4 and I execute a `push eax` instruction, what address will ESP now be pointing to?



#### What is a stack frame?

A stack frame is a portion in the stack section of data that stores the local variables of the currently running functions, the return address to go when the function exits, and the old stack pointer before the function was called. 

#### What would you find in a data section?

In the data section, you would find the statically defined variables and the global variables of the program.

#### What is the heap used for?


#### What is in the code section of a program's virtual memory space?

#### What does the `inc` instruction do, and how many operands does it take?

It increments the value in a register by 1. It takes 1 operand.

#### If I perform a `div` instruction, where would I find the remainder of the binary division (modulo)?

You would find the remainder of the binary division in the register: EDX. 

#### How does `jz` decide whether to jump or not?

#### How does `jne` decide whether to jump or not?

#### What does a `mov` instruction do?

A 'mov' instruction can:
- copy a value to a register. 
- copy the value in a register to a register. 
- copy the value in a memory location to a register. 

#### What does the `TF` flag do and why is it useful for debugging?

When TF flag is set, the processor will only execute one instruction at a time. 

When debugging, we may want to find the effect of each instruction or try to find which instructions causing certain changes in the system. However, an x86 processor may have multiple threads or cores, so multiple executions can be executed parallely which make it difficult to identify the right instructions.

Thus, by only allowing one instruction to execute at a time, it makes it easier to debug. As a result, the TF is useful for debugging. 

#### Why would an attacker want to control the EIP register inside a program they want to take control of?

#### What is the AL register and how does it relate to EAX?

#### What is the result of the instruction `xor eax, eax` and where is it stored?

The result of 'xor eax, eax' is 0, and the value is stored in the register eax. 


#### What does the `leave` instruction do in terms of registers to leave a stack frame?

#### What `pop` instruction is `retn` equivalent to?

#### What is a stack overflow?

#### What is a segmentation fault (a.k.a. a segfault)?

#### What are the ESI and EDI registers for?

