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

if __name__ == "__main__":
    while True:     
        username = input("Input your desired username: ")
        if len(username) < 8 or len(username) > 12:
            continue
        
        passwd = get_passwd(username)
        print("The password is", passwd)
        break