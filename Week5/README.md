# Week 5

In week 5, we did some more practices on disasseblying programs using the tools (Ghidra) and knowledge learned in Week 4.  

## Ghidra Lab

### Executive Summary


### Evidence
input: 0123456789012345678
input: 0000000000000000000
Answer:0v50-0000-0000-0u70

input 

rock: 
input >=  0x2D and (input >= 0x2D or input > 0x40)
(input < 0x3A or input > 0x40)
(input <= 0x5A or input >= 0x61) and  (input <= 0x7A)
|input| == 19

rules: 
input >=  0x2D and (input >= 0x2D or input > 0x40)
(input < 0x3A or input > 0x40)
(input <= 0x5A or input >= 0x61) and  (input <= 0x7A)

=> 
input >=  0x2D
(input < 0x3A or input > 0x40)
(input <= 0x5A or input >= 0x61) and (input <= 0x7A)

=> 
input >=  0x2D
(input < 0x3A or input > 0x40)
(input <= 0x5A and input <= 0x7A) or (input >= 0x61 and input <= 0x7A)

=>
input >=  0x2D
(input < 0x3A or input > 0x40)
(input <= 0x5A) or (input >= 0x61 and input <= 0x7A)

=>
(input >=  0x2D and input < 0x3A) or (input >=  0x2D and input > 0x40)
(input <= 0x5A or input >= 0x61) and (input <= 0x5A or input <= 0x7A)

=> 
(input >=  0x2D and input < 0x3A) or (input > 0x40)
(input <= 0x5A or input >= 0x61) and (input <= 0x7A)

=>
[(input >=  0x2D and input < 0x3A) or (input > 0x40)] and (input <= 0x5A or input >= 0x61) and (input <= 0x7A) 

paper: 
A = input[10] xor input[8] + 0x30
B = input[13] xor input[5] + 0x30

0x30 <= A < 0x3a and 0x30 <= B < 0x3a

input[3] == A and input[15] == A
input[0] == B and input[18] == B

Rules:
0x30 <= A, B, input[3], input[15], input[0], input[18] < 0x3a
0 <= input[10] xor input[8] <= 9
0 <= input[13] xor input[5] <= 9

scissor: 
A = input[2] + input[1]
B = input[17] + input[16]

A >= 0xab and B >= 0xab
A != B 

cracker:
input[14] + input[4] + input[9] == 0x87

=> 0x2D + 0x2D + 0x2D = 0x87

If input[14], input[4], or input[9] is any number greater than 0x2D, we will get values greater than 0x87.

So, input[14] == input[4] == input[9] = 0x87

