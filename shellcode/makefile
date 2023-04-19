all: shellcode shellcode_test
	./shellcode_test
#./shellcode
shellcode: shellcode.S
	as shellcode.S -o shellcode.o
	ld shellcode.o -o shellcode --oformat=binary
	rm shellcode.o
#--oformat=binary

shellcode_test: shellcode_tester.c	 
	gcc shellcode_tester.c -o shellcode_test -z execstack -no-pie
