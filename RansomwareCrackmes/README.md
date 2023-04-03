# Binary Reverse Engineering with Crackmes 

In this week, we did some more practices on disasseblying programs using the tools (Ghidra). In this week, the programs were modified so that we cannot use uftrace.  

## Ghidra Lab

### ransomware_1 Solution (): 

Run the below code with the encrypted file path as a command-line argument to decrypt the file. 
The codes for the decryptor to decrypt is: 

```python
# ransomware 1

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
```

#### How I did it using Ghidra: 

password: 
I figured out the password by looking at the program in Ghidra. By tracing the input from getinput(), I know that the input was passed as an argument to a function along with a static string "lumpy_cactus_fruit". This suggested to me that the password was "lumpy_cactus_fruit", testing it showed that it was indeed true. However, the password only gave me the docx file. There is still secret.txt. 
Thus, I attempted to figure out the decryption scheme below.

decrypt():
1. I opened the crackme in Ghidra. 
2. I saw that there are many functions whose names did not make sense. These functions are the result of Ghidra not being able to distinguish between an argument pushed onto stack, and a normal push command. Thus, for these functions, I did some forward engineering to try to guess what an attacker would write and guess based on some of the used parameters shown. For example, I know that the functions, printing out a string matching with the ones saw when running the ransomware, must be printf. 
3. I was given a hint of the other unknown function in main() to be the free() to free the character pointer. 
4. I look at the decrypt function to figure out how it decryps. 
5. I noticed that it was accepting what seemed like an input file name, output file name, and their length. I know this because they were passing static string. Thus, I renamed and retyped those variables. 
6. From running the program, I knew that the behaviour of the ransomware is that it takes the encrypte file and decrypt it to a separate file. 
7. Thus, I knew that there must be calls to fopen(), fread(), and fwrite() to do these things. 
8. I saw that there is a function taking the infile name and outfile name as the argument, as well as a static string of "rb" and "wb". Thus, I renamed and retyped that function to that of fopen().
9. I saw the printf function again, and it printed out a variable as "Decrypting file %s. It is %d bytes long". This suggested that the variable for %d must be the length of the read in file. I renamed that variable to file_length. 
10. By googling about how to get file length, I know that we must use fseek() to get to the end, and ftell() to get the size. Based on that, I retyped the function around the places that set the variable file_length. 
11. I know that after using fseek() to read the file again, I must reset the read pointer, so there must have been the function rewind(). Thus, I reypted the function called right after calling ftell() to be rewind(). 
12. Now, the program opens the write file in write mode and enter the for loop. I noticed that the for loop was looping file_length times. Thus, using forward engineering, I know that we must be calling fread() in each iteration, decrypt it, then write it to the outfile. 
13. Since there are file_length iterations, it must mean that we only read 1 byte at a time. 
14. Inside the for loop, I saw 2 functions called. I know that it must be fread() followed by fwrite(). Thus, I retyped and renamed those 2 functions. This showed that a byte was read in a variable; I renamed that variable. Then, before being written to the outfile, the byte was being XORed with '4'. 
15. As a result, the decryption scheme is that we read in each byte, xor each byte with '4'. 
16. I tested with the secret.text and got an intelligible file. However, I don't know what the original file content was. Better ask the client!!!

The decrypted result of secret.text.payup is:

        Dear Student,

        You have decrypted the message. Good job!

        "Many of the engineers I interviewed worked on reverse-engineering technology. Itâs a hallmark of Area 51."
        ~ ANNIE JACOBSEN

        Go NMSU RE!


### ransomware_2 Solution (): 

Run the below code with the encrypted file path as a command-line argument to decrypt the file. 
The codes for the decryptor to decrypt is: 

```python
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

```

#### How I did it using Ghidra: 

password: 
I figured out the password by looking at the program in Ghidra. By tracing the input from getinput(), I know that the input was passed as an argument to a function along with a static string "delicious". This suggested to me that the password was "delicious", testing it showed that it was indeed true. However, the password only gave me the docx file. There is still secret.txt. 
Thus, I attempted to figure out the decryption scheme below.

decrypt():
1. I opened the crackme in Ghidra. 
2. I saw that there are many functions whose names did not make sense. These functions were the result of Ghidra not being able to distinguish between an argument pushed onto stack, and a normal push command. Thus, for these functions, I did some forward engineering to try to guess what an attacker would write and guess based on some of the used parameters shown. For example, I know that the functions, which prints out a string matching with the ones seen when running the ransomware, must be printf. 
3. Since the password was the string "delicious" as mentioned, then the function must be strcmp. This can be confirmed because the return value of strcmp was checked if it was not 0 (not equal), then we print out that the password was incorrect. 
4. Using some forward engineering and since this program is similar to ransomware_1, I know that the function FUN_00011170 must be free(). 
5. I then found the decrypt() in the else case where we got the right password. It was inputing the name of the encrypted docx and the name of the decrypted docx. Thus, I know that this must be the function to figure out to find the encryption/decryption scheme. 
6. I changed the function signature:
    + Change type from EVP_PKEY_CTX to char *, since it was passing the string before. 

7. Looking at the behaviour of the program with the docx file, I knew that the function must  have been reading the encrypted file and write the decrypted output to the decrypted file. I did not see it in the main function, so it must have happened in the decrypt function. Thus, I'm expecting to see in the decrypted function: fopen(), fread() and fwrite().

8. However, there are functions whose names did not make sense in decrypt (similar to point 2). Thus, some of them must be the functions mentioned. 

9. I see that there was a printf call that prints out the number of bytes long of the encrypted file, so I updated the signature to accept 3 arguments and it revealed that local_28 was being put as the number of bytes. I renamed it to infilesize. 

10. I see that infilesize was set to the return value of a function. Using my knowledge of C, I know that to get the file lsize, one could use ftell, so I guess that the function was ftell. 

11. Changing the signature of the function to that of ftell() revealed that local_2c was passed as the input, so it must be the FILE pointer. 

12. I then saw that the FILE pointer was set by the first function call in decrypt(), so it must be fopen(). Changing the signature to that of fopen() showed that it was indeed the case, because the second argument of the function was "rb", meaning read binary. 

13. I saw that fopen() was also called later on with "wb" and outfile name, so it was opening the file to write the decrypted output. 

14. There were some unknown functions before reaching fopen() for the outfile. Using my knowledge of C, I know that when openning the file, the file position must be at the beginning, so before using ftell() to get the size, I must get to the final file position, which can be done using fseek(). Then, before reading the encrypted content, we must go back to the starting file position. so rewind() must be used. Thus, I renamed the 2 weird names functions close to ftell() to fseek() and rewind(). Changing the signature to that of the 2 functions showed that it was indeed the case because one of the argument was the infilepointer. 

15. Looking at the codes after openning the outfile. Based on the behaviour when decrypting the docx file, I know that we must avoid the printf of the error message. This means that we need to go to code_r0x00011519 at the end of the decryption. Thus, we will loop in the do-while loop a couple of times, then goto code_r0x00011519 while still not finishing the loop at the end of the decryption.

16. To go to code_r0x00011519, I know that local_20 must be equal to 0. I then know that to decrypt, we must use fread() and then fwrite(). I guessed that the function whose return value was set for local_20 was fread(). Changing the signature showed that it was indeed the case because infilepointer was an argument for the function. 

17. Then, the other function must be fwrite(). Changing the signature showed that it was indeed the case because outfilepointer was an argument. 

18. I see that the conditional for the do-while loop was that the number of bytes written had to be the same as the number bytes read. 

19. Thus, the for loop inside the do-while loop must have been the decryption codes. It was true because local_15 was modified inside the for loop and its content was written later on. 

20. Looking at the arguments for fread(), I saw that local_15 was the buffer, so I renamed it. I also renamed the variables in the for loop to make it more familiar. 

21. I can see that we were looping from [0, bytes_read] and set
    buf[i] = buf[i] ^ local_34[i]

22. However, since we only read/write 4 bytes at a time (the size of each element was 1 byte and the number of elements read/written was 4), which can be seen from the arguments of fread() and fwrite(). This becomes:
    buf[0] = buf[0] ^ local_34[0]
    buf[1] = buf[1] ^ local_34[1]
    buf[2] = buf[2] ^ local_34[2]
    buf[3] = buf[0] ^ local_34[3]

23. I see that local_34 was the string "1337". Thus, this becomes:
    buf[0] = buf[0] ^ '1'
    buf[1] = buf[1] ^ '3'
    buf[2] = buf[2] ^ '3'
    buf[3] = buf[0] ^ '7' 

24. As a result, the decryption scheme was that we get every 4 bytes, and XOR each of the 4 bytes as shown above. 

25. Using this decryption scheme to decrypt secret.txt.payup showed an intelligible string. Thus, this must be the correct decryption scheme. 

The decrypted result of secret.text.payup is:

            Dear Student,

            You have decrypted the message. Good job!

            "Basically, if reverse engineering is banned, then a lot of the open source community is doomed to fail."
            ~ Jon Lech Johansen

            Go NMSU RE!


### ransomware_3 Solution (): 

Run the below code with the encrypted file path as a command-line argument to decrypt the file. 
The codes for the decryptor to decrypt is: 

```python
# ransomware 3
import sys

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
                byte = byte ^ ord('R')
            elif count == 2:
                byte = byte ^ ord('3')
            elif count == 3:
                byte = byte ^ ord('V')
            elif count == 4:
                byte = byte ^ ord('3')
            elif count == 5:
                byte = byte ^ ord('R')
            elif count == 6:
                byte = byte ^ ord('5')
            elif count == 7:
                byte = byte ^ ord('3')
                count = 0
                
            decrypted_bytes.append(chr(byte))
            byte = f.read(1)
            count += 1
    
    print("".join(decrypted_bytes))
```

#### How I did it using Ghidra: 

password: 
I figured out the password by looking at the program in Ghidra. By tracing the input from getinput(), I know that the input was passed as an argument to a function along with a static string "delicious". This suggested to me that the password was "delicious", testing it showed that it was indeed true. However, the password only gave me the docx file. There is still secret.txt. 
Thus, I attempted to figure out the decryption scheme below.

decrypt():
1. I opened the crackme in Ghidra. 
2. I saw that there are many functions whose names did not make sense. These functions were the result of Ghidra not being able to distinguish between an argument pushed onto stack, and a normal push command. Thus, for these functions, I did some forward engineering to try to guess what an attacker would write and guess based on some of the used parameters shown. For example, I know that the functions, which prints out a string matching with the ones seen when running the ransomware, must be printf. 
3. Since the password was the string "delicious" as mentioned, then the function must be strcmp. This can be confirmed because the return value of strcmp was checked if it was not 0 (not equal), then we print out that the password was incorrect. 
4. Using some forward engineering and since this program is similar to ransomware_1, I know that the function FUN_00011170 must be free(). 
5. I then found the decrypt() in the else case where we got the right password. It was inputing the name of the encrypted docx and the name of the decrypted docx. Thus, I know that this must be the function to figure out to find the encryption/decryption scheme. 
6. I changed the function signature:
    + Change type from EVP_PKEY_CTX to char *, since it was passing the string before. 

7. Looking at the behaviour of the program with the docx file, I knew that the function must  have been reading the encrypted file and write the decrypted output to the decrypted file. I did not see it in the main function, so it must have happened in the decrypt function. Thus, I'm expecting to see in the decrypted function: fopen(), fread() and fwrite().

8. However, there are functions whose names did not make sense in decrypt (similar to point 2). Thus, some of them must be the functions mentioned. 

9. I see that there was a printf call that prints out the number of bytes long of the encrypted file, so I updated the signature to accept 3 arguments and it revealed that a variable was being put as the number of bytes. I renamed it to infilesize. 

10. I see that infilesize was set to the return value of a function. Using my knowledge of C, I know that to get the file lsize, one could use ftell, so I guess that the function was ftell. 

11. Changing the signature of the function to that of ftell() revealed that a variable was passed as the input, so it must be the FILE pointer. 

12. I then saw that the FILE pointer was set by the first function call in decrypt(), so it must be fopen(). Changing the signature to that of fopen() showed that it was indeed the case, because the second argument of the function was "rb", meaning read binary. 

13. I saw that fopen() was also called later on with "wb" and outfile name, so it was opening the file to write the decrypted output. 

14. There were some unknown functions before reaching fopen() for the outfile. Using my knowledge of C, I know that when openning the file, the file position must be at the beginning, so before using ftell() to get the size, I must get to the final file position, which can be done using fseek(). Then, before reading the encrypted content, we must go back to the starting file position. so rewind() must be used. Thus, I renamed the 2 weird names functions close to ftell() to fseek() and rewind(). Changing the signature to that of the 2 functions showed that it was indeed the case because one of the argument was the infilepointer. 

15. I saw that a variable named key was being printed along with the string "Restored key", so it must have been a key. The key was of type char *. 

16. Then, I looked at the do-while loop. I knew using forward engineering that the do-while needs to fread() to read some bytes from the encrypted file, decrypt those bytes, and write those files to the decrypted file. 

17. Thus, the first function in do-while loop would be fread(). Retyping the function showed that it was indeed true because infile was an argument of the function. I see that fread() was reading in 7 elements, each element is 1 byte, so 7 bytes read. lb

18. As a result, the decryption scheme was that we get every 4 bytes, and XOR each of the 4 bytes as shown above. I also renamed the first argument to buf to denote a buffer. 

19. I see that I want to avoid the error message, the number of bytes read must be equal to 0 to go to code_r0x000115d2. This happens when we are at the end of the file. 

20. Thus, the function after this if-conditional must be the fwrite function as it is the only other function call. Retyping the function showed that it was indeed true because outfile was an argument for the output file. 

21. Thus, the codes in between must have been the decryption code. 

22. I see that for each element in the buffer of size 7 (index i):

        buf[i] = buf[i] ^ key[i]

23. I see that key was gotten from a function which I renamed to getkey(). However, getkey() is another one of those functions where it jumps to a different location instead of having codes. I decided to look at the closely related function, restore_key() which is a normal function. I retyped its signature to the signature to its actual signature (I know this by looking at the signature when double-clicking on the function). 

24. It revealted that it accepts the address of the char * HIDDEN_KEY (it is the string "S4W4S64") with the address of key (which is char *). Thus, the final type of the parameters would be char **.  

25. Looking at restore_key, I know that the restore_key seemed to use the values of key. Thus, getkey() may actually be just a function to allocate memory. Retyping the signature of restore_key to char** revealed that restore_key was simply:
    key[i] = hiddenkey[i] - 1. 

    Thus, the key is just simply R3V3R53 since hidden key is a fixed string, which is the exact same key printed by the program. 

26. Thus, the decryption becomes:

        buf[0] = buf[0] ^ 'R'
        buf[1] = buf[1] ^ '3'
        buf[2] = buf[2] ^ 'V'
        buf[3] = buf[3] ^ '3'
        buf[4] = buf[4] ^ 'R'
        buf[5] = buf[5] ^ '5'
        buf[6] = buf[6] ^ '3'

27. Thus, the decryption scheme is simply just reading 7 bytes and XOR each byte with the mentioned mechanism. 

28. Using this decryption scheme to decrypt secret.txt.payup showed an intelligible string. Thus, this must be the correct decryption scheme. 

The decrypted result of secret.text.payup is:

        Dear Student,

        You have decrypted the message. Good job!

        "A good engineer thinks in reverse and asks himself about the stylistic consequences of the components and systems he proposes."
        ~ Helmut Jahn

        Go NMSU RE!

