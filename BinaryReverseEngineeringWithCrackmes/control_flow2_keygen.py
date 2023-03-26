# control flow 2
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