#include <stdio.h>

int main(void) {
	int array[10];
	printf("%p\n", array);
	printf("%p\n", &array[1]);
	printf("%p\n", &array[2]);
} // end main
