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