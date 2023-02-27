# Week 5

In week 5, we did some more practices on disasseblying programs using the tools (Ghidra) and knowledge learned in Week 4.  

## Ghidra Lab
### Crackme 1 Solution (http://crackmes.cf/users/seveb/crackme05/download/crackme05.tar.gz): 
To solve this crackme, you need to put a right serial code that matches certain conditions as the first command-line argument of the crackme program when running the program. 

There are 4 rounds of criteria that the serial code needs to pass:

1. Rock
2. Paper
3. Scissor 
4. Cracker

My solution is to create a Python3 program that will randomly generate correct serial code although it will not cover all possible codes. 

To run the program, put the codes for the program (below) to a file and run it with python3. 
For example, put the codes in main.py and run "python3 main.py".

The codes for the serial code generator are: 
        
        # program to get the serial code for for crackme 1
        from random import randint

        def rock_rule(num):
            # line 10
            # line 14
            # line 15
            return ((num >=  0x2D) and ((num <= 0x2D) or (num > 0x30)))\
                    and ((num < 0x3A) or (num > 0x40))\
                    and (((num <= 0x5A) or (num >= 0x61)) and  (num <= 0x7A))

        def check_paper(num1, possible_nums):
            def check(num2):
                temp = num1 ^ num2
                num = (temp + 0x30)
                return temp >= 0 and temp <= 9 and (num in possible_nums) and num >= 0x30 
            
            return check

        def check_scissor(num1):
            def check(num2):
                temp = num1 + num2
                return temp >= 0xab 
            
            return check


        def get_result(nums):
            result = []
            for i in range(len(nums)):
                result.append(chr(nums[i]))
            return "".join(result)

        result = list(range(19))

        # rock
        possible_nums_rock = list(range(0x7F))
        possible_nums_rock = list(filter(rock_rule, possible_nums_rock))


        # get rock
        for i in range(len(result)):
            result[i] = possible_nums_rock[randint(0, len(possible_nums_rock) -1)]

        print("pass rock:", get_result(result))

        # get paper
        while True:
            will_pass = check_paper(result[10], possible_nums_rock)
            if will_pass(result[8]): # pass the test
                break

            # check for other options
            temp = list(filter(will_pass, possible_nums_rock))
            if len(temp) <= 0: # no other options try a different value
                result[10] = possible_nums_rock[randint(0, len(possible_nums_rock) -1)]
                result[8] = possible_nums_rock[randint(0, len(possible_nums_rock) -1)]
                continue
            
            # find at least one option
            result[8] = temp[randint(0, len(temp) - 1)]

        # found the right option for 10 and 8
        result[13] = result[10]
        result[5] = result[8]

        # A and B can be the same
        val = (result[10] ^ result[8]) + 0x30

        result[3] = val 
        result[15] = val 
        result[0] = val
        result[18] = val


        print("pass paper: ", get_result(result))

        # pass scisor

        while True:
            check_2 = check_scissor(result[2])
            check_17 = check_scissor(result[17])
            A = result[2] + result[1]
            B = result[17] + result[16]

            if not check_2(result[1]): # pass the test
                # check for other options
                temp = list(filter(check_2, possible_nums_rock))
                if len(temp) <= 0: # no other options try a different value
                    result[2] = possible_nums_rock[randint(0, len(possible_nums_rock) -1)]
                    result[1] = possible_nums_rock[randint(0, len(possible_nums_rock) -1)]
                    continue

                result[1] = temp[randint(0, len(temp) - 1)]
                #print("asdf", result[1], check_2(result[1]), temp)
            
            # check results[17]
            if not check_17(result[16]):
                temp = result[2] + 1
                if temp not in possible_nums_rock:
                    continue

                result[17] = temp
                result[16] = result[1]
            
            # check A != B
            if A != B:
                break

        print("pass scissor:", get_result(result))
        print("2", check_scissor(result[2])(result[1]))
        print("17", check_scissor(result[17])(result[16]))
        # pass cracaker

        result[4] = 0x2D
        result[14] = 0x2D
        result[9] = 0x2D

        print("pass cracker:", get_result(result))

### How I did it using Ghidra: 

1. I opened the crackme in Ghidra. 
2. I looked for the "main" function that has 2 parameters. Thus, using my knowledge of C program, I know that those must be argc for the number of command-line arguments and argv containing the strings of the arguments. 

    Then, I see that argv[1] is passed as an argument for 4 functions, rock(), scissor(), paper(),j and cracker(). 
    
    Looking at the code of each of these functions, I know that they all call a function called bomb() that prints some stuffs and exit. Thus, this must be the program that I need to avoid in order to not prematurely exit. 

    If I can run pass these 4 functions without exiting, I will finally go to decraycray() function, which will only print stuffs before succesfully exiting.

    As a result, I know that I must pass the 4 functions to solve this crackme. 

3. Looking at rock(), I know that to avoid bomb(), I need to skip the first "if", get into the "else if", fail the inner "if", and fail the final "if". From this I found out that: 


        Assumes input is our serial code.  

        Using a little bit of discrete math, I found that to pass rock: 
        ((input >=  0x2D) and ((input <= 0x2D) or (input > 0x30)))
        and ((input < 0x3A) or (input > 0x40))
        and (((input <= 0x5A) or (input >= 0x61)) and  (input <= 0x7A))
        and input.length == 19

4. Looking at paper(), I know that to avoid bomb(), I need to get into the first "if", fail the inner "if", get into the second "if", fail the inner "if": 

        I found that to pass paper:
        A = input[10] xor input[8] + 0x30
        B = input[13] xor input[5] + 0x30

        (0x30 <= A < 0x3a) 
        and (0x30 <= B < 0x3a)

        input[3] == A and input[15] == A
        input[0] == B and input[18] == B

        We can then derive that:
        0x30 <= A, B, input[3], input[15], input[0], input[18] < 0x3a
        0 <= (input[10] xor input[8]) <= 9
        0 <= (input[13] xor input[5]) <= 9

        **In my solution, I assigned A to be equal to B to simplify the task**

5. Looking at scissor(), I know that to avoid bomb(), I need to avoid the first "if" and the "else if": 

        To pass scissor: 
        A = input[2] + input[1]
        B = input[17] + input[16]

        (A >= 0xab and B >= 0xab)
        and (A != B)

6. Looking at cracker(), I know that to avoid bomb(), I need to avoid the first "if": 

        To pass cracker:
        input[14] + input[4] + input[9] == 0x87

        => 0x2D + 0x2D + 0x2D = 0x87

        If input[14], input[4], or input[9] is any number greater than 0x2D, we will get values greater than 0x87.

        So, input[14] == input[4] == input[9] = 0x87



