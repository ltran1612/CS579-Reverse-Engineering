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

#### How I did it using Ghidra: 

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


### Crackme 2 Solution (http://crackmes.cf/users/adamziaja/crackme1/download/crackme1.tar.gz): 

To solve this crackme, you need to extract the password generated from the username you entered. 

My solution is to create a Python3 program that will generate a password based on an input username. 

To run the program, put the codes for the program (below) to a file and run it with python3. 
For example, put the codes in main.py and run "python3 main.py".

The codes for the password generator are:

        # Crackme 2 Solution
        # Author: Long Tran
        
        # A function to get the password from the username. 
        def get_passwd(username):
            temp_str = ""

            # Point 5 in the readme
            for i in range(len(username)):
                temp = ""
                if (i & 1) == 0:
                    temp = username[i].lower()
                else:
                    temp = username[i].upper()
                
                temp_str += str(ord(temp))
            
            # Point 7 in the readme
            temp_str = temp_str[(len(username) - 8) * 2:]

            # Point 9 in the readme
            temp_str = temp_str[0:8]

            # Point 11 in the readme
            result = ""
            for c in temp_str:
                if c.isdigit():
                    result += c
                elif result != "" and not c.isdigit():
                    break
            
            result = int(result)

            return result

        # Starting Point
        if __name__ == "__main__":
            while True:     
                username = input("Input your desired username: ")
                if len(username) < 8 or len(username) > 12:
                    continue
                
                passwd = get_passwd(username)
                print("The password is", passwd)
                break

When running the program, it will ask you for the username you want to use, then it will generate a password and prints it out on the screen. 

#### How I did it using Ghidra: 
It was shown to be written in C++ in Ghidra. 

1. I looked for the "main" function because it's our starting point. 
2. I went back and forth between lines of codes, looking at both the analyzed C++ version and the assembly. I found out that the way that it was translated by Ghidra was quite confusing so it took me a while to guess what the lines mean. For example, we have this line of code:

        "uVar6 = (ulong), uVar4 = std::basic_string<char,std::char_traits<char>,std::allocator<char>>::length(), uVar6 < uVar4"

It was initialy not clear for me what's string of which we are taking the length. However, looking at the aseembly code that showed that we were loading the address of string username into a register before calling lenght() suggested that it was the length of username we're looking for. 
Thus, this statement is: "i < username.length()".

3. Initially, the program was printing "username must be between 8 and 12" and use cin to read input in username. It also output the prompt "serial number: " and input a serial number from cin. 
4. Then, it checks if the length is greater than 8 and less than 12. 
5. It loops from 1 to the length of the username string: 
    - It converts username[i] (for index i) to lowercase if (i bitwise and 1) is 0; that is, if i is a binary number such that the least significant bit is not 0. Since our maximum length is 12 and minimum length is 8. Such indexs are: 1, 3, 5, 7, 9, 11.  
    - It converts username[i] (for index i) to upercase otherwise.  
    - In both cases, it will add it to a stream with "<<". I intially thought that it was going to cast the char to a string to add it to the stream, but using gdb showed otherwise. Thus, **it will add the string of the integer ASCII value of the converted character to the list**. For example, if the ASCII value is 45, then it will add "45" to the string. 

6. The new string from step 5 is called serialString.
7. We calculate the substring from (username.length() - 8) * 2 to -0x1 (which is the largest integer value). This means that the substring from the calculated position till the end.
8. Assign the substring to serialString
9. It loops from 0 to 8 (8 not included):
    - get serialString[i] and add it to the end of serialString2. Before the loop, serialString2 was not set, so by default according to cpp documentation, it will be an empty string. Link: https://cplusplus.com/reference/string/string/string/
    
    Thus, we are taking the substring of serialString from 0 to 8 and make it serialString2. 

10. Create a basic_istringstream from serialString2. 
11. Extract number in the stringstream to the integer serial. According to the documentation for the >> operator of basic_istringstream. It will extract a number from the string ignore whitespaces, if there are no numbers, it will return 0. Link: https://en.cppreference.com/w/cpp/io/basic_istream/operator_gtgt
12. Compare the extracted number with the input serial:
    - if the same, we print "OK"
    - else: we print "WRONG"

### Crackme 5 Solution (http://crackmes.cf/users/seveb/crackme04/download/crackme04.tar.gz): 
