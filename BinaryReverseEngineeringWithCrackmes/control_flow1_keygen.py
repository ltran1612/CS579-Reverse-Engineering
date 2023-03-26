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