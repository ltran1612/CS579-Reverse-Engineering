# Binary Reverse Engineering with Crackmes 

In this week, we did some more practices on disasseblying programs using the tools (Ghidra, uftrace).  

## Ghidra Lab
### ezcrackme1.zip Solution (https://nmsu.instructure.com/courses/1524743/files/215427565?wrap=1): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the "main" function that has 2 parameters. 

### ezcrackme2.zip Solution (https://nmsu.instructure.com/courses/1524743/files/215427602?wrap=1): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the "main" function that has 2 parameters. 

### ezcrackme3.zip Solution (): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the "main" function that has 2 parameters. 

### controlflow_1.zip Solution (): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the sink of my program by starting at main, and try to go functions that will avoid printing error message and non-0 exit codes. The result I found is that we need to go as follows: main() -> rock() -> paper() -> scissor() -> lizard() -> spock() -> win() to get to the correct goal, which exit(0).  
3. Now that I know where to get, I lookek back in the "main" function to find the conditions to reach there. The main functions accept command-line arguments. I renamed the main() arguments to match the C-standard; that is, argc and argv. I noticed that the program get the first argument through accessing argv[1] (call this input). 
4. Then, it gets the parameter string length with strlen(). The program then compares if the length is less than 16. If it is, errors, else we go to rock. 
Thus, len(input) > 16
5. I went to rock(). Knowing that we pass in the argument, I retyped the argument type of rock() to char*. This helped me clearly see that the function was reading in the character at index 3, or the 4th character of input. 
6. Then, to get to our next goal: paper(), that character must not be equal to 'Z', 'Z' >= the ASCII value of that character (called this input[3]), 'K' >= input[3], 'J' > input[3], and input[3] == '2'. This means that input[3] == '2'.
7. In paper(), to get to our next goal: scissors(), by retyping the just like in rock(), I see that we need:

        + input[7] - 0x25 < 0x2e => input[7] < 0x2e + 0x25
        + calculation = 1 << (byte) [(input[7] - 0x25) & 0x3f] -- cast to (byte) means we only get the least significant 8 bits of the calculation before using it in shifting.
        + calculation & 0x280110000000  == 0 and calculation & 1 != 0
8. In scissors(), to get to our next goal: lizard(), we need the following:

        + input[0] < 0x54
        + input[0] < 0x52 and input[0] != 0x49
        + 0x49 >= input[0]
        + input[0] == 0x41



### controlflow_2.zip Solution (): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the "main" function that has 2 parameters. 

### controlflow_3.zip Solution (): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the "main" function that has 2 parameters. 



