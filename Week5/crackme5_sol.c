#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

int hex35478 = 0x35478;
char * str8_char = "7030726e";

int main(int argc, char ** argv) {
    if (argc < 2) {
        perror("Input the path to the test program as the argument");
        exit(1);
    } // end if

    const char * crackme5 = argv[1];
    int process_id = 0x539;

    // create pipe
    int read_pipe[2];
    if (pipe(read_pipe) < 0) {
        perror("failed to create pipe");
        exit(1);
    } // end if

    int write_pipe[2];
    if (pipe(write_pipe) < 0) {
        perror("failed to create pipe");
        exit(1);
    } // end if

    // create child process
    int c_pid = fork();
    if (c_pid == 0) { // child process
        close(read_pipe[1]); // close the writing end
        close(write_pipe[0]); // close the reading end

        int rfds = read_pipe[0]; // get the reading end
        int wfds = write_pipe[1];  // get the writing end

        // change stdin and stdout
        if (dup2(rfds, STDIN_FILENO) == -1 || dup2(wfds, STDOUT_FILENO) == -1) {
            fprintf(stderr, "Child: Failed to change input to pipe\n");
            close(wfds);
            close(rfds);
            exit(1);
        } // end if
        
        fprintf(stderr, "Child: process is running...\n");

        char * arg[0];
        if (execl(crackme5, crackme5, NULL) < 0) {
            fprintf(stderr, "Child: process failed to run: %s\n", crackme5);
            close(wfds);
            close(rfds);
            exit(1);
        } // end if
    } else { // parent process
        close(read_pipe[0]);
        close(write_pipe[1]);

        process_id = c_pid;
        printf("Parent: The child process id is %d\n", process_id);

        // generate the key
        int temp;
        char str_buf [356];
        char str2[1000];
        // set str2 to elements of 0 value.
        for (int i = 0; i < 1000; ++i) {
            str2[i] = '\0';
        } // end for i

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
        printf("Parent: The serial code is %s\n", str2);

        // write the serial code
        printf("Parent: Try the serial code with the crackme program...\n");
        // get the length of the string to write

        // check if the child process still exists before inputing 
        int status;
        if (waitpid(c_pid, &status, WNOHANG | WUNTRACED) == -1) {
            fprintf(stderr, "Parent: Child process stopped.\n");
            exit(1);
        } // end if

        int rfds = write_pipe[0];
        int wfds = read_pipe[1]; 

        int bw = write(wfds, str2, str2Length);
        // check if we have written successfully.
        if (bw == -1) {
            fprintf(stderr, "Parent: Failed to input the serial code to the crackme program.\n");
            exit(1);
        } // end if
        bw = write(wfds, "\n", 1);
        if (bw == -1) {
            fprintf(stderr, "Parent: Failed to input the newline to the crackme program.\n");
            exit(1);
        } // end if

        fprintf(stderr, "Parent: Sucessfully sent the serial code\n");
        // read all outputs from the child process
        int sr;
        char buff[1000];
        do {
            sr = read(rfds, buff, 1000);
            buff[sr] = '\0';
            printf("CHILD OUTPUT:\n%s", buff);
        } while(sr > 0);

        close(wfds);
        close(rfds);
    } // end else


} // end main