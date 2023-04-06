# program to get the serial code for crackme 1
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
print("final pass is", get_result(result))


