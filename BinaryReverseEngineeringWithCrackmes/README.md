# Binary Reverse Engineering with Crackmes 

In this week, we did some more practices on disasseblying programs using the tools (Ghidra, uftrace).  

## Ghidra Lab
### ezcrackme1.zip Solution (https://nmsu.instructure.com/courses/1524743/files/215427565?wrap=1): 

The password is "picklecucumberl337". There is no need for a keygen because that is the only password for this crackme.

#### How I did it:  
1. I used `uftrace` with the "-a" flag to see the arguments of function calls and got the following output with the initial input of "test": 

                # DURATION     TID     FUNCTION
                0.350 us [  6681] | __monstartup();
                0.160 us [  6681] | __cxa_atexit();
                        [  6681] | main() {
                108.878 us [  6681] |   puts("Please insert the password:") = 28;
                        [  6681] |   getinput() {
                2.185  s [  6681] |     getline();
                1.333 us [  6681] |     strlen("test\n") = 5;
                2.185  s [  6681] |   } /* getinput */
                0.953 us [  6681] |   strcmp("test", "picklecucumberl337") = 4;
                3.549 us [  6681] |   printf("Your password <%s> was incorrect. Time for som>
                0.411 us [  6681] |   free(0x563784820820);
                2.186  s [  6681] | } /* main */

2. Looking at the output, I saw that my input was compared with "picklecucumberl337". This suggested that the only password could the string "picklecucumberl337".
3. I tested "picklecucumberl337" and it was the correct password.  

### ezcrackme2.zip Solution (https://nmsu.instructure.com/courses/1524743/files/215427602?wrap=1): 

The password is "artificialtree". There is no need for a keygen because that is the only password for this crackme. 

#### How I did it: 
1. I used `uftrace` with the "-a" flag to see the arguments of function calls and got the following output with the initial input of "test": 

                # DURATION     TID     FUNCTION
                0.491 us [  6736] | __monstartup();
                0.161 us [  6736] | __cxa_atexit();
                        [  6736] | main() {
                104.979 us [  6736] |   puts("Please insert the password:") = 28;
                        [  6736] |   getinput() {
                1.145  s [  6736] |     getline();
                1.504 us [  6736] |     strlen("test\n") = 5;
                1.145  s [  6736] |   } /* getinput */
                1.263 us [  6736] |   strcmp("test", "artificialtree") = 19;
                4.511 us [  6736] |   printf("Your password <%s> was incorrect. Time for som>
                0.561 us [  6736] |   free(0x5637bdc15820);
                1.145  s [  6736] | } /* main */
             
2. Looking at the output, I saw that my input was compared with "artificialtree". This suggested that the only password could the string "artificialtree".
3. I tested "artificialtree" and it was the correct password.  

### ezcrackme3.zip Solution (https://nmsu.instructure.com/courses/1524743/files/215427617?wrap=1): 
The only password is "strawberrykiwi", so there is no need for a keygen. 

#### How I did it using Ghidra:  
1. I opened the crackme in Ghidra. 
2. Starting from the main() function, I looked for what could be my sink() based on the output message and I found that the sink() is when we print "you craked me" along with "Now make a keygen!". 
3. Tracing backward, I found that the conditions are: 

        + !bVar3
        + (local_40 != 0) and (!bVar3) and (iVar1 != 0) and (iVar2 != 0)
        
        => (local_40 != 0) and (!bVar3) and (iVar1 != 0) and (iVar2 != 0)
        <=> (local_40 != 0) and (bVar3 == 0) and (iVar1 != 0) and (iVar2 != 0)
4. I saw that bVar3 = (iVar2 != 0) before iVar2 was updated. So the conditions become (iVar2_old is the iVar2 before changing and iVar2_new is the iVar2 after changing):

        (local_40 != 0) and ((iVar2_old != 0) == 0) and (iVar1 != 0) and (iVar2_new != 0) 

        <=> (local_40 != 0) and (iVar2_old == 0) and (iVar1 != 0) and (iVar2_new != 0) 

5. I saw that iVar2_old was the result of strcmp, between local_38 and loca_48. 
6. I saw that the address of local_48 was passed as an argument to getinput(). The function name suggests that it is used to get input from the keyboard. 
7. Searching Google did not show any API of this function. However, from my knowledge of C, I know that either a character pointer must be passed to this function to store the string, or it returns a pointer. 
8. getinput() did not return any value in the codes, so it must be the former case. 
9. Since local_48 was used as a comparison and its address was passed as the argument for getinput(). My guess is that local_48 is used to store the input from the keyboard. So, I renamed it to "input".  
10. iVar1 = strcmp(input, "kiwi"). For iVar1 to not be 0, input must not be the string "kiwi". Thus, the updated condition is: 

        (local_40 != 0) and (iVar2_old == 0) and (input is not the string "kiwi") and (iVar2_new != 0) 

11. iVar2_new = strcmp(input, "strawberry"). input was not modified after gotten from the keyboard. This means that input is not the string "strawberry". Thus, the updated condition is: 

        (local_40 != 0) and (iVar2_old == 0) and (input is not the string "kiwi") and (input is not the string "strawberry") 

12. iVar2_old = strcmp(input, (char *)&local_38). This suggests that the address of local_38 is a character pointer. Thus, the type of local_38 must be a character. So, I reypted it to char. 

13. I saw that the program use strcat on local_38, which was to add string to the end of a string. It added "strawberry" and "kiwi". Initially, local_38 was set to 0. Thus, my guess is that after the two concatenation operations, local_38 is the string "strawberrykiwi". 

14. iVar2_old == 0 means that the input must be the string "strawberrykiwi". Thus, the updated condition could be: 
        
        (local_40 != 0) and (input is the string "strawberrykiwi") and (input is not the string "kiwi") and (input is not the string "strawberry") 

15. The address of local_40 was passsed as an argument to getinput(). Since local_48 was our guess to store the input. Then, maybe local_40 was used to store the length of the number of characters read. This makes sense because character pointer does not store the length of the array, so we need a second variable to store that information. Thus, our updated condition could be: 

        (input length is not 0) and (input is the string "strawberrykiwi") and (input is not the string "kiwi") and (input is not the string "strawberry") 

        <=> input is the string "strawberrykiwi"

16. Testing the string "strawberrykiwi" as the password showed that it worked. 

17. I did not see any other codes suggesting other passwords. Thus, "strawberrykiwi" is the only password for this crackme. 

### controlflow_1.zip Solution (https://nmsu.instructure.com/courses/1524743/files/215491475?wrap=1): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running this program.

The codes for the keygen to generate those serial codes are: 

                import random
                # our starting possible values
                values = list(range(ord('0'), ord('z')+1))
                values.remove(ord('`'))

                if __name__ == "__main__":
                        # make sure the length is greater than or equal  16
                        answer = random.choices(values, k=16)

                        # rock()
                        answer[3] = ord('2')

                        # paper()
                        # first condition
                        choices = list(filter(lambda x: x < (0x2e + 0x25), values))
                        
                        # second condition
                        answer[7] = 0x25
                        
                        # scissors()
                        answer[0] = 0x41

                        # lizzard()
                        answer[1] = ord('6')

                        # spock()
                        answer[15] = ord('*')

                        answer = ''.join(map(lambda x: chr(x), answer))
                        print("answers:",answer)

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the sink of my program by starting at main, and try to go functions that will avoid printing error message and non-0 exit codes. The result I found is that we need to go as follows: main() -> rock() -> paper() -> scissor() -> lizard() -> spock() -> win() to get to the correct goal, which exit(0).  
3. Now that I know where to get, I lookek back in the "main" function to find the conditions to reach there. The main functions accept command-line arguments. I renamed the main() arguments to match the C-standard; that is, argc and argv. I noticed that the program get the first argument through accessing argv[1] (call this input). 
4. Then, it gets the parameter string length with strlen(). The program then compares if the length is less than 16. If it is, errors, else we go to rock. 
Thus, len(input) > 16
5. I went to rock(). Knowing that we pass in the argument, I retyped the argument type of rock() to char*. This helped me clearly see that the function was reading in the character at index 3, or the 4th character of input. 
6. Then, to get to our next goal, paper(), that character must not be equal to 'Z', 'Z' >= the ASCII value of that character (called this input[3]), 'K' >= input[3], 'J' > input[3], and input[3] == '2'. This means that input[3] == '2'.
7. In paper(), to get to our next goal, scissors(), by retyping the just like in rock(), I see that we need:

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

9. In lizard(), go get to our next goal, spock(), we need the following based on the switch statement:

        + input[1] == '6'
10. In spock(), to get to our final goal, win(), we need the following based on the switch statement:

        + input[15] == '*'

Finally, we reach win() and there is nothing to do here. 

### controlflow_2.zip Solution (https://nmsu.instructure.com/courses/1524743/files/215492029?wrap=1): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

The codes for the keygen to generate those serial codes are: 

                import random
                # our starting possible values
                values = list(range(ord('0'), ord('z')+1))
                values.remove(ord('`'))

                if __name__ == "__main__":
                        # make sure the length is greater than or equal  16
                        answer = random.choices(values, k=16)

                        #    1. input[8] == 0x23
                        #   2. input[11] == '*'
                        #   3. input[10] == 'A'
                        #   4. input[13] == '6'
                        #   5. input.length >= 16
                        #   6. input[6] ==  'Y'

                        answer[8] = 0x23

                        answer[11] = ord('*')
                        answer[10] = ord('A')
                        answer[13] = ord('6')
                        answer[6] = ord('Y')

                        answer = ''.join(map(lambda x: chr(x), answer))
                        print("answers:",answer)

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

### controlflow_3.zip Solution (https://nmsu.instructure.com/courses/1524743/files/215427731?wrap=1): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

The codes for the keygen to generate those serial codes are: 

                import random
                # our starting possible values
                values = list(range(ord('0'), ord('z')+1))
                # removed so we don't need to worry about escaping for this one
                values.remove(ord('`'))


                if __name__ == "__main__":
                        # make sure the length is greater than or equal  16
                        answer = random.choices(values, k=16)
                        
                        # rock()
                        # paper()
                        # lizard()
                        # spock()
                        while True:
                                # rock
                                one = random.choice(values)
                                three = random.choice(values)
                                five = random.choice(values)
                                six_choices = list(filter(lambda x: x == one + three - five, values))

                                if len(six_choices) == 0:
                                continue

                                answer[1] = one
                                answer[3] = three
                                answer[5] = five
                                answer[6] = random.choice(six_choices)

                                # paper
                                six = answer[6]
                                seven_choices = list(filter(lambda x: six ^ x < 0x03, values))
                                if len(seven_choices) == 0:
                                continue

                                answer[7] = random.choice(seven_choices)

                                # lizard()
                                seven = answer[7]
                                eight_choices = list(filter(lambda x: seven ^ x >= 0x04, values))
                                if len(eight_choices) == 0:
                                continue
                                answer[8] = random.choice(eight_choices)


                                # spock()
                                eight = answer[8]
                                nine_choices = list(filter(lambda x: eight != x, values))
                                if len(nine_choices) == 0:
                                continue
                                answer[9] = random.choice(nine_choices)

                                # spock() and scissors()
                                # case1 
                                # from scissors input[12] == input[10]
                                case1 = list(filter(lambda x: (x < 0x03)
                                                and (x ^ answer[8] ^ answer[9]) != 1, values))

                                if len(case1) > 0:
                                answer[10] = random.choice(case1)
                                answer[12] = answer[10]
                                break

                                # case2
                                case2 = list(filter(lambda x: (x >= 0x03)
                                                and (x ^ answer[8] ^ answer[9]) != 0, values))
                        
                                if len(case2) > 0:
                                answer[10] = random.choice(case2)
                                answer[12] = answer[10]
                                break
                        
                        # answer
                        answer = ''.join(map(lambda x: chr(x), answer))
                        print("answers:",answer)

#### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked to find where the sink is searching for a code that prints something like a final result and exit with exit code of 0. I found that the sink is win(). 
3. To reach to win(), we need to go to spock(). I found this by searching for references of win(), and the only function calling win() is spock().   
4. To reach to spock(), by using the same method, I know that only lizard() called spock(). 
5. To get to lizard(), by using the same method, I know that scissors(), spock(), and lizard() call lizard(). So, we need to get to scissors().
6. To get to scissors(), by using the same method, I know that paper() call scissors(). So, we need to reach paper().
7. To get to paper(), by using the same method, I know that rock() call paper(). So, we need to reach rock().
8. To get to rock(), by using the same method, I know that main() call rock(). So, we need to get to rock() from main().  
9. So the general flow is main() -> rock() -> paper() -> scissors() -> lizard() -> spock() -> win().
10. Looking at main(), I know that the program gets the first command-line argument (I call input). Then, it checks the length of input with 16. If the length is smaller than 16, or the length is greater than 16, the program errors. If the length is 16, we call rock() with input as the argument. Thus, the condition to call rock() is input.length == 16.
11. From rock(), to get to paper(), by updating the parameter type of rock() from long to char*, I found the following conditions: 

        (input[1] + input[3] - ipnut[5]) == input[6]
        
12. From paper(), to get to scissors(), by doing the same thing as with rock(), I found the following conditions:

        input[6] ^ input[7] < 0x03

13. From scissors(), to get to lizard(), by doing the same thing, I found the following conditions:

        input[10] == input[12]

14. From lizard(), to get to spock(), by doing the same thing, I found the following conditions:

        input[8] ^ input[7] >= 0x04

15. From spcok(), to get to our final goal: win(), by doing the same thing, I found the following conditions: 

        input[8] != input[9]
        (input[12] ^ input[8] ^ input[9]) != (input[10] < 0x03)
        => case 1: (input[10] < 0x03). So, LHS != 1 (True)
        => case 2: (input[10] >= 0x03). So, LHS != 0 (False)
        There are two cases, so we only need to test both. 

16. Thus, I used these conditions to create a keygen that will randomly pick values from the ASCII tables until all of the conditions are satisfied. 