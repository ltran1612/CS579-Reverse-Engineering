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
        + calculation & 0x280110000000  == 0  
        + calculation & 1 != 0 => this means that the last bit must be 1

        This means that calculation must has the last bit to be 1. Since we left shift 1, the only time when we get such a case is when we don't shift at all. So, calculation must be 1 << 0. 
        Thus, (byte)[(input[7] - 0x25) & 0x3f] = 0 
        => input[7] - 0x25 = 0
        => input[7] = 0x25

8. In scissors(), to get to our next goal: lizard(), we need the following:

        + input[0] < 0x54
        + input[0] < 0x52 and input[0] != 0x49
        + 0x49 >= input[0]
        + input[0] == 0x41

This means that input[0] == 0x41. 

9. In lizard(), go get to our next goal: spock(), we need the following based on the switch statement:
        + input[1] == '6'
10. In spock(), to get to our final goal: win(), we need the following based on the switch statement:
        + input[15] == '*'

Finally, we reach win() and there is nothing to do here. 

### controlflow_2.zip Solution (): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked to find where the sink is searching for a code that prints something like a final result and exit with exit code of 0. I found that the sink is win(). 
3. To reach to win(), we need to go to spock(). I found this by searching for references of win(), and the only function calling win() is spock().   
4. To reach to spock(), by using the same method, I know that only lizard() called spock(). 
5. To get to lizard(), by using the same method, I know that scissors(), spock(), and lizard() call lizard(). So, we need to get to scissors().
6. To get to scissors(), by using the same method, I know that rock(), paper(), and scissors() call scissors(). So, we either need to reach either rock() or paper() with certain inputs.
7. So the general flow is main() -> ..something.. -> scissors() -> lizard() -> spock() -> win(). 
8. We will look at the individual condition for the ones that we know first. 
9. From scissors(), to get to the lizard(). It has a switch statement that suggests that the parameter type is actually a char * instead of long. Thus, changing the type, shows that the following condition is needed to get to lizard() from scissors():
    + argument[10] == 'A'

10. From lizard(), to get to spock(), similar to scissors(), the following condition is needed:
    + argument[13] = '6'

11. From spock(), to get to win(), similar to the other 2 cases, the following condition is needed:
    + argument[11] = '*'

12. To get to scissors() from rock(), it called scissors(&DAT_00102081). However, DAT_00102081 is the char array [4, 4, null]. However, looking at the condition for scissors(), we know that this will not get us to lizard(), so this call is not correct. Thus, the only to get to scissors() is from paper(). 

13. To get to paper(), by checking the references, the only option is to go from rock(). 

14. To get to rock(), by checking references, the most feasible option is to go from main(), which is our source. 

15. The flow is: main() -> rock() -> paper() -> scissors() -> lizard() -> spock() -> win(). 

16. The condition to get to scissors() from paper() is:
        + argument[8] - 0x23 < 0x38 => argument[8] < 0x38 + 0x23
        + uVar1 = 1 << ((byte)((int) argument[8] - 0x23) & 0x3f) -- byte casting, so 1 is only left shifted 8 times. 
        + uVar1 & 0xa8000080000000 == 0 => uvar1 & 0 == 0, which is always true. 
        + uVar1 & 1 == 0 => this means that the last bit of uVar1 is 1. This only happens if there was no left shifting at all. It means that (((int) argument[8] - 0x23) & 0x3f) == 0 => argument[8] - 0x23 == 0 
        => argument[8] == 0x23.  

17. To get from rock() to paper(). We need the following conditions:
        + argument[6] != '~'
        + argument[6] <= '~'
        + argument[6] == 'Y'
        => argument[6] == 'Y' (since 'Y' < '~')
18. To get from main() to rock(), we got the first command-line argument and check if its length is less than 16. Thus, we need the following conditions:
        + input.length >= 16

18. Looking at main(), we pass to rock the first command-line argument. Looking at rock(), paper(), scissors(), and lizard(). We pass to the next function, the same argument without changing anything. As a result, the argument is just the input. 

As a result, the conditions are: 
1. input[8] == 0x23
2. input[11] == '*'
3. input[10] == 'A'
4. input[13] == '6'
5. input.length >= 16
6. input[6] ==  'Y'

### controlflow_3.zip Solution (): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the "main" function that has 2 parameters. 



