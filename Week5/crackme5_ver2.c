#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

u_int32_t hex35478 = 0x35478;
char * str8_char = "7030726e";

int main(int argc, char ** argv) {
    if (argc < 2) {
        perror("Input the path to the test program as the argument");
        exit(1);
    } // end if

    const char * crackme5 = argv[1];
    int process_id = getpid();

    // generate the key
    int temp;
    char str_buf [356];
    char str2[1000];

    // set str2 to elements of 0 value.
    for (int i = 0; i < 1000; ++i) {
        str2[i] = '\0';
    } // end for i

    // calculating the key
    int str2Length;
    for (int i = 0; i < 7; ++i) {
        hex35478 = process_id ^ hex35478;
        temp = hex35478 + str8_char[i] + 0x5c;
        temp = temp ^ 4;
        hex35478 = hex35478 | 0x2e39f3;
        sprintf(str_buf,"%d",temp);
        str2Length = strlen(str_buf);
        strncat((char *)str2,str_buf,str2Length);
        hex35478 = hex35478 << 7;
    } // end for i

    str2Length = strlen(str2); 
    str2[str2Length] = '\0';
    printf("The serial code is %s\n", str2);

    char * arg[0];
    if (execl(crackme5, crackme5, NULL) < 0) {
        fprintf(stderr, "command failed to run: %s\n", crackme5);
        exit(1);
    } // end if

} // end main