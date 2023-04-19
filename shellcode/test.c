#include <unistd.h>

int main(void) {
    char str[1];
    str[0] = '\0';
    char *dummy[1];
    dummy[0] = NULL;
    
    char *argv[] = {'\0'};
    execve("/bin/sh", dummy, dummy);
}