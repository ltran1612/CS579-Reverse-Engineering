import sys
# ransomware 2

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("no file name")
        exit(1)

    file_name = sys.argv[1]
    decrypted_bytes = []
    count = 0
    with open(file_name, "rb") as f:
        byte = f.read(1)
        count += 1
        while byte != b"":
            byte = int.from_bytes(byte, byteorder="little")
            if count == 1:
                byte = byte ^ ord('1')
            elif count == 2:
                byte = byte ^ ord('3')
            elif count == 3:
                byte = byte ^ ord('3')
            elif count == 4:
                byte = byte ^ ord('7')
                count = 0
                
            decrypted_bytes.append(chr(byte))
            byte = f.read(1)
            count += 1
    
    print("".join(decrypted_bytes))