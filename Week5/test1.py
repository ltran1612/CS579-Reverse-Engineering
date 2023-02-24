result = range(19)

def rock_rule(num):
    return ((num >=  0x2D and num < 0x3A) or (num > 0x40)) and (num <= 0x5A or num >= 0x61) and (num <= 0x7A) 

# pass rock
possible_nums = range(0x7F)
result = list(filter(rock_rule, possible_nums))


# pass cracaker
result[4] = 0x2D
result[14] = 0x2D
result[9] = 0x2D

print(result)
