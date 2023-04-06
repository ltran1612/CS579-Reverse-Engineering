#include <stdio.h>

int main(void) {
    char s[1000];
    printf("child program\n");
    scanf("%s", s);
    printf("Found %s\n", s);
} // end main