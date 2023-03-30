# Binary Reverse Engineering with Crackmes 

In this week, we did some more practices on disasseblying programs using the tools (Ghidra). In this week, the programs were modified so that we cannot use uftrace.  

## Ghidra Lab

### ransomware_1 Solution (): 


The codes for the decryptor to generate those serial codes are: 

```python

```

#### How I did it using Ghidra: 

password: 
I figured out the password by looking at the program in Ghidra. By tracing the input from getinput(), I know that the input was passed as an argument to a function a long with a static string "lumpy_cactus_fruit". This suggested to me that the password was "lumpy_cactus_fruit", testing it showed that it was indeed true. However, the password only gave me the docx file. There is still secret.txt. 
Thus, I attempted to figure out the decryption scheme below.

decrypt():
1. I opened the crackme in Ghidra. 
2. I saw that there are many functions whose names do not make sense. These functions are the result of Ghidra not being able to distinguish between an argument pushed onto stack, and a normal push command. Thus, for these functions, I did some forward engineering to try to guess what an attacker would write and guess based on some of the parameters used shown. For example, I know that the functions, printing out a string matching with the ones saw when running the ransomware, must be printf. 
3. I was given a hint of the other unknown function in main() to be the free() to free the character pointer. 
4. I look at the decrypt function to figure out how it decryps. 
5. I noticed that it was accepting what seemed like an input file name, output file name, and their length. I know this because they were passing static string. Thus, I renamed and retyped those variables. 
6. From running the program, I know that the behaviour of the ransomware is that it takes the encrypte file and decrypt it to a separate file. 
7. Thus, I know that there must be calls to fopen(), fread(), and fwrite() to do these things. 
8. I saw that there is a function taking the infile name and outfile name as the argument, as well as a static string of "rb" and "wb". Thus, I renamed and retyped that function to that of fopen().
9. I saw the printf function again, and it prints out a variable as "Decrypting file %s. It is %d bytes long". This suggested that the variable for %d must be the length of the read in file. I renamed that variable to file_length. 
10. By googling about how to get file length, I know that we must use fseek() to get to the end, and ftell() to get the size. Based on that, I retyped the function around the places that set the variable file_length. 
11. I know that after using fseek() to read the file again, I must reset the read pointer, so there must be the function rewind(). Thus, I reypted the function called right after calling ftell() to be rewind(). 
12. Now, the program opens the write file in write mode and enter the for loop. I noticed that the for loop was looping file_length times. Thus, using forward engineering, I know that we must be calling fread() in each iteration, decrypt it, then write it to the outfile. 
13. Since there are file_length iterations, it must mean that we only read 1 byte at a time. 
14. Inside the for loop, I saw 2 functions called. I know that it must be fread() followed by fwrite(). Thus, I retyped and renamed those 2 functions. This showed that a byte was read in a variable; I renamed that variable. Then, before being written to the outfile, the byte was being XORed with '4'. 
15. As a result, the decryption scheme is we read in each byte, xor each byte with '4'. 
16. I tested with the secret.text and got a intelligible file. However, I don't know what the original file was, I don't know what the file is. Better ask the client!!!