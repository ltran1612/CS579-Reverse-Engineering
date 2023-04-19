all: shellcode shellcode_test
	./shellcode_test
shellcode: shellcode.S
	as shellcode.S -o shellcode.o
	ld shellcode.o -o shellcode 
	rm shellcode.o

shellcode_test: shellcode_tester.c	 
	gcc shellcode_tester.c -o shellcode_test -z execstack -no-pie
