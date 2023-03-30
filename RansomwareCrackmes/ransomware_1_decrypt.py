import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("no file name")
        exit(1)

    file_name = sys.argv[1]
    decrypted_bytes = []
    with open(file_name, "rb") as f:
        byte = f.read(1)
        while byte != b"":
            byte = int.from_bytes(byte, byteorder="little")
            byte = byte ^ ord('4')
            decrypted_bytes.append(chr(byte))
            byte = f.read(1)
    
    print("".join(decrypted_bytes))