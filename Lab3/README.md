# Week 3 - Running the Malware

This week, I learned how to set up a fake Internet using inetsim.
However, before setting the Internet, I had to change the malware run environment from Windows 10 to Windows XP. This was because according to the Professor, Windows 10 can block all of the malwares in this lab. 

Now, to set up the fake internet, I first created a virtual network with a DHCP server in VirtualBox. Then, I created another linux virtual machine (I chose Debian) to run inetsim. I then connect the 2 virtual machines to the created virtual network so that the Windows XP machine can communicate with the linux machine. 

Then, in the Windows XP, I added the IP address of the linux machine as the DNS server on the Windows machine so that DNS requests from the Windows machine will be resolved by the linux machine. 

---
# Lab 3-1 

## Executive Summary

Using static analysis on the malware shows that:
1) It is trying to connect to a website: "www.practicalmalwareanalysis.com"
2) It is trying to run some programs and exit some proccesses. 
3) It tries to run some kernel-level operations. 
4) The malware is packed with "PEncrypt 3.1 Final -> junkcode"

Using dynamic analysis showed us that the malware added a VideoDriver registry with value ""C:\WINDOWS\system32\vmx32to64.exe". Also, the running program is the same malware that is started. 
I also confirmed that the malware connect to "www.practicalmalwareanalysis.com" using a SSL protocol with an unknown version to inetsim. 

## Indicators of Compromise

**Compilation Date (according to VirusTotal):** 2008-01-06 14:51:31 UTC

**MD5 Hash of the EXE file:** d537acb8f56a1ce206bc35cf8ff959c0

**Network Communication to Look for:** Connection to this URL: "www.practicalmalwareanalysis.com"

**Process Name to Look for:** Lab03-01.exe

## Mitigations

- Delete files that match these files's hash. 

## Evidence - static analysis

This virus has one file: Lab03-01.exe

I examined the malware with the following tools:

### VirusTotal

Checking with VirusTotal showed that this file was marked by 66 security vendors to be malicious. 

### strings

Using strings showed us that:
1) The malware uses kernel32.dll library.
2) The string "CONNECT %s:%i HTTP/1.0", showed that it tried to connect to some website using HTTP/1.0 protocol. The "%s" and "%i" seems to be placeholder in printf string functions in C. I then saw the string "www.practicalmalwareanalysis.com", showing that this could be the website the malware is trying to connect to. 

I also saw the following strings: 
1) "SOFTWARE\Microsoft\Windows\CurrentVersion\Run": This suggests that the program tries to run some programs.
2) "SOFTWARE\Classes\http\shell\open\commandV"
3) "Software\Microsoft\Active Setup\Installed Components\"'
4) "SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folderes"
4) "WinUMX32-": Looking on the Internet showed no information about this file, suggesting that this is not a file that Windows uses. 
5)"vmx32to64.exe": Looking on the Internet showed no information about this file, suggesting that this is not a file that Windows uses. 
6) "ExitProcess": This is a function in the kernel32.dll

Thus, this showed us that this malware could be trying to run some programs and exit.

### PEiD

Using PEiD gave us "PEncrypt 3.1 Final -> junkcode", showing that this malware was packed with PEncrypt 3.1 Final.
This is an encryptor online with this value, but there was no decryptor for it. 
Thus, with the current techniques, I cannot decrypt this file to look for more information. 

This suggests the maliciousness of the program as a typical normal program does not have a need to pack their softwares. 

### PEViewer 

Using PEViewer helped confirm the information got with "strings" that ExitProcess is a function in the kernel32.dll

### Dependency Walker

Using dependency walker revealed that the malware also uses "ntdll.dll" library inside "kernel32.dll". According to computerhope.com, "ntdll.dll" contains NT kernel functions.
According to Wikipedia, NT kernel mode is the kernel mode that can control "scheduling, thread priotitization, memory management" (Wikipedia), and can interact with hardware.

These operations are very powerful suggesting that the malware may try to affect threads scheduling and memory management, or even interacting with hardwares. 

Link: 
+ computerhope.com: https://www.computerhope.com/issues/ch000960.htm. Retrieved on Feb 14, 2023.
+ wikipedia: https://en.wikipedia.org/wiki/Architecture_of_Windows_NT. Retrieved on Feb 14, 2023.


## Evidence - dynamic analysis

### Procmon

Using procmon shows that the malware executes the following tasks: 
1) Load an image.
3) Call CreateFile operations with the following files (all in system32 folder): advpack.dll
2) Changing registries.
4) Send a TCP request to "www.inetsim.org".

### Process Explorer

Using the strings tab on Process Explorer showed me "VideoDriver" string. 
Also, the content in the strings is similar to that of the original program, so this must be running the same program. 

### Regshot

Using regshot showed us that 25 registries were changed and 3 were added after running the malware.
One of the registry has the same subfolder as the one I saw in strings, while 2 of the registries changed also had subfolders similar to the values found using strings.  The rest of the registries seemed to be from wireshark as they are related to tcpip. This was due to me getting the order of executions wrong. 

The added registry is: "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\VideoDriver" with the value when converted from hex to utf-16 is "C:\WINDOWS\system32\vmx32to64.exe". I also saw this .exe in strings. Thus, this malware added a VideoDriver registry with the value "C:\WINDOWS\system32\vmx32to64.exe". 

The value of the 2 modified registries are "01 00 00 00 43 00 00 00 70 B7 8B E9 05 41 D9 01". However, converting this to UTF-16, UTF-8, Unicode, and ASCII only gave us gibberish values.


### wireshark + inetsim

Using wireshark showed us that the malware tries to make a query to "www.practicalmalwareanalysis.com". 
Then, looking at inetsim, I saw that the malware is trying to make a SSL connection. However, inetsim was not able to set up a communication due to the error "SSL attempt failed: 140routines:ssl3_get_record:wrong version number".
Thus, it seemed like the malware is connecting with an older version of SSL. 

---
# Lab 3-2

## Executive Summary

Using static analysis, we knew the following:
1) Access the website "practicalmalwareanalysis.com" using GET request of HTTP 1.0 protocol. 
2) It's trying to acces and change the registry of the system. 
3) It creates a service which will be hosted under svhost.exe, and uninstall, and delete the service some time later. 
4) It's used for a GUI program. 
5) It creates some threads, procceses, and pass data between them.  
6) The program was written in C++. 
7) It's trying to run some java programs.


## Indicators of Compromise

**Compilation Date (according to VirusTotal):**  2010-09-28 01:00:25 UTC 

**MD5 Hash of the EXE file:** 84882c9d43e23d63b82004fae74ebb61

## Mitigations

- Delete files that match these files's hash. 

## Evidence

This virus has one file: Lab03-02.dll

I examined the malware with the following tools:

### VirusTotal

Checking with VirusTotal showed that this file was marked by 56 security vendors to be malicious. 

### strings


#### Component Analysis

Using strings showed us a lot of gibberish strings with some useful strings:
1) GetModuleFileNameA: 

2) These strings suggest that the malware is trying open threads and proccesses, and pass data between procceses. 
    + Sleep, TerminateThread, CreateThread, GetProcAddress, WaitForSingleObject, CreateProcessA, GetStartupInfoA
    + GetSystemTime, CreatePipe

3) These files suggest that the malware is trying to load a library, read in some files: LoadLibraryA, GetLongPathNameA, GetTempPathA, ReadFile, CloseHandle, GetCurrentDirectoryA.

4) The strings below suggest that the malware is trying to print out some errors:

    + GetLastError 
    + SetLastError
    + OutputDebugStringA

5) The strings below suggest that the malware tries to edit the registries of the system:

    + ADVAPI32.dll
    + RegSetValueExA
    + RegCreateKeyA
    + RegCloseKey
    + RegQueryValueExA
    + RegOpenKeyExA
    + RegOpenKeyEx(%s) KEY_QUERY_VALUE success.
    + RegOpenKeyEx(%s) KEY_QUERY_VALUE error .

6) The strings below suggest that the malware tries to create a new service, run it, and delete the service:

    + RegisterServiceCtrlHandlerA
    + CloseServiceHandle
    + CreateServiceA
    + OpenSCManagerA
    + DeleteService
    + OpenServiceA
    + SetServiceStatus
    + Install
    + ServiceMain
    + UninstallService
    + installA
    + uninstallA
    + DependOnService
    + ServiceDll
    + %SystemRoot%\System32\svchost.exe -k: According to Wikipedia, this is a proccess that is shared among multiple services to run each of them. 
    + SYSTEM\CurrentControlSet\Services\
    + CreateService(%s) error %d
    + %SystemRoot%\System32\svchost.exe -k netsvcs
    + OpenSCManager()
    + You specify service name not in Svchost//netsvcs, must be one of following:
    + RegQueryValueEx(Svchost\netsvcs)
    + netsvcs
    + SOFTWARE\Microsoft\Windows NT\CurrentVersion\Svchost
    + OpenService(%s) error 2
    + OpenService(%s) error 1

***Link: https://en.wikipedia.org/wiki/Svchost.exe. Retrieved on Feb 14, 2023***

7) The strings below suggests that this malware tries to dynamically load a DLL:

    + WSASocketA
    + WS2_32.dll

8) This suggests that the program is trying to access this website: "practicalmalwareanalysis.com":

    + InternetReadFile
    + HttpQueryInfoA
    + HttpSendRequestA
    + HttpOpenRequestA
    + InternetConnectA
    + InternetOpenA
    + InternetCloseHandle
    + WININET.dll
    + practicalmalwareanalysis.com
    + serve.html: Maybe this is the html file that the malware is trying to access. 
    + GET: The website is accessed through a HTTP GET method. 
    + HTTP/1.1
    + Intranet Network Awareness (INA+)


9) These strings suggest that hte progrma was written in C and it tries to read/write some files and edit/make some new strings:
    + memset, wcstombs, strncpy, strcat, strcpy, atoi, fclose, fflush, fwrite, fopen, strrchr, atol, sscanf, strlen, strncat, strstr, free, malloc, strchr, MSVCRT.dll
    + lstrlenA

10) This suggests that the program using this dll will try to access this dll:
    + Lab03-02.dll

11) Some other suspicious looking strings: 
    + Windows XP 6.11
    + kernel32.dll
    + .exe
    + %s %s
    + 1234567890123456
    + cmd.exe /c 
    + ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
    + .PAX
    + .PAD
    + RpcSs
    + GetModuleFileName() get dll path
    + ErrorControl
    + DisplayName
    + Description

12) The below strings suggest that this dll is used for a GUI program because it has ImagePath:

    + Depends INA+, Collects and stores network configuration and location information, and notifies applications when this information changes.
    + ImagePath
    + IPRIP
    + uninstall success
    + uninstall is starting

#### Summary of strings
The summary of strings show us that this malware will:
1) Access the website "practicalmalwareanalysis.com" using GET request of HTTP 1.0 protocol. 
2) It's trying to acces and change the registry of the system. 
3) It creates a service which will be hosted under svhost.exe, and uninstall, and delete the service some time later. 
4) It's used for a GUI program. 
5) It creates some threads, procceses, and pass data between them.  
6) The program was written in C++. 

### PEiD

Using PEiD showed us "Microsoft Visual C++ 6.0 DLL \[Overlay\]", suggesting that the malware was written in C++. Along with the function names saw with "strings", this seems to be indeed the case. 

According to user "Git" on reteam.org, this suggests that the malware was compiled with Microsoft VC 6.0 and linked in Overlay mode. According to Wikipedia, Overlay means to transfer a block of memory on the main memory of a process. Thus, the former statement means that the library will be linked by putting its code in the main memory.

Hence, this malware does not seem to be packed. 

Link:
1) reteam.org: http://www.reteam.org/board/showthread.php?t=2749. Retrieved on Feb 14, 2023
2) wikipedia https://en.wikipedia.org/wiki/Overlay_(programming). Retrieved on Feb 14, 2023

### PEViewer 

Using PEViewer showed that this .dll exported the following functions: 
1) Install
2) ServiceMain
3) UninstallSErvice
4) InstallA
5) uninstallA

### Dependency Walker

Using Dependency Walker errored that it could not load and find msjava.dll. This suggests that the malware is trying to run some java programs. 

## Evidence - dynamic analysis

### Procmon

### Process Explorer

### regshot

### wireshark + inetsim

---
# Lab 3-3

## Executive Summary

Using static analysis, we know that: 
    + This malware seems to be creating a GUI program. 
    + This program seems to try to read/modify some files. 
    + This malware seems to access to some resources.
    + This malware seems to create a new process and copy some memory from one process to another.
    + The malware seems to run/access svchost.exe, which is a process used to run multiple services, as well as modify scheduling or memory management.
    + This malware was written in C++. 

## Indicators of Compromise

**Compilation Date (according to VirusTotal):**  2011-04-08 17:54:23 UTC 

**MD5 Hash of the EXE file:**  e2bf42217a67e46433da8b6f4507219e 

## Mitigations

- Delete files that match these files's hash. 

## Evidence

This virus has one file: Lab03-03.exe

I examined the malware with the following tools:

### VirusTotal

Checking with VirusTotal showed that this file was marked by 58 security vendors to be malicious. 

### strings


#### Component Analysis
Using "strings" showed us a lot of gibberish strings with a couple of readable information:

1) The strings below suggest that the malware is trying to print out a variety of errors: 
    + runtime error 
    + TLOSS error
    + SING error
    + DOMAIN error
    + R6028
    + - unable to initialize heap
    + R6027
    + - not enough space for lowio initialization
    + R6026
    + - not enough space for stdio initialization
    + R6025
    + - pure virtual function call
    + R6024
    + - not enough space for _onexit/atexit table
    + R6019
    + - unable to open console device
    + R6018
    + - unexpected heap error
    + R6017
    + - unexpected multithread lock error
    + R6016
    + - not enough space for thread data
    + abnormal program termination
    + R6009
    + - not enough space for environment
    + R6008
    + - not enough space for arguments
    + R6002
    + - floating point not loaded
    + Microsoft Visual C++ Runtime Library
    + Runtime Error!
    + <program name unknown>
    + user32.dll: According to ProcessLibrary, user32.dll is a library for handling user interface. Link: https://www.processlibrary.com/en/directory/files/user32/19597/. Retrieved on Feb 14, 2023
    + GetLastActivePopup
    + GetActiveWindow
    + MessageBoxA

2) These strings below suggest that this malware is trying to modify some files: 
    + CloseHandle
    + VirtualFree
    + ReadFile
    + VirtualAlloc
    + GetFileSize
    + CreateFileA

3) These strings suggest that this malware is creating a new process and copy some memory from one process to another, and that other process could be from running another program:
    + ResumeThread
    + SetThreadContext
    + WriteProcessMemory: According to Microsoft, this function is used to copy a piece of memory from one process to a specified process. Link: https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory. Retrieved from (Feb 14, 2023)
    + VirtualAllocEx
    + GetProcAddress
    + GetModuleHandleA
    + ReadProcessMemory
    + GetThreadContext
    + CreateProcessA
    + GetCommandLineA
    + GetVersion
    + ExitProcess
    + TerminateProcess
    + GetCurrentProcess
    + Sleep

4) These strings suggest that this malware is trying to access some computing resources: 
    + FreeResource
    + SizeofResource
    + LockResource
    + LoadResource
    + FindResourceA
    + GetSystemDirectoryA

5) This suggests that the malware is trying to run/access svchost.exe, which is a process used to run multiple services, as well as modify scheduling or memory management. This is because ntdll.dll is a library that contains the functions to do those tasks: 
    + \svchost.exe
    + NtUnmapViewOfSection
    + ntdll.dll

#### Summary of strings

In summary, we know from strings that: 
    + This malware seems to be creating a GUI program. 
    + This program seems to try to read/modify some files. 
    + This malware seems to access to some resources.
    + This malware seems to create a new process and copy some memory from one process to another.
    + The malware seems to run/access svchost.exe, which is a process used to run multiple services, as well as modify scheduling or memory management.

### PEiD

Using PEiD on the program showed us that it uses "Microsoft Visual C++ 6.0". This suggests that the program was not packed. It also suggests that the program was written in C++. 

### PEViewer

Using PEViewer did not show any useful information to me. 

### Dependency Walker

Using Dependency Walker showed similar to "strings" that the malware uses KERNEL32.dll and NTDLL.dll

---
