# Week 1 - Simple Static Analysis

---
# Lab 1-1 

## Executive Summary
Lab01-01.exe and Lab01-01.dll seem to be a type of malware that can create a backdoor. 

It also seems to copy a file to the system32 folder and disguise that file as kernel32.dll. 

It also seems to communicate with the IP address "127.26.152.13".

However, to study the effect of the malware, I need more analysis. 

## Indicators of Compromise

**Compilation Date (according to VirusTotal):** 2010-12-19 16:16:19 UTC

**MD5 Hash of the EXE file:** bb7425b82141a1c0f7d60e5106676bb1 

**MD5 Hash of the DLL file:** 290934c61de9176ad682ffdd65f0a669 

**File to look for:** `C:\windows\system32\kerne132.dll`

**Network Communication to look for:**
Network communication with the IP address: `127.26.152.13`

## Mitigations

- Delete files that match these files's hash. 
- Scan Windows machines for `system32\kerne132.dll`
- Check network for communication to `127.26.152.13`. 

## Evidence

This malware has 2 files: a lab01-01.exe and a lab01-01.dll. 

I examined the malware with the following tools:

### VirusTotal
These 2 files were flagged by 49 and 42 security vendors as malicious, respectively.

### strings

- #### .EXE: 

I found this string "WARNING_THIS_WILL_DESTROY_YOUR_MACHINE" indicating that it must come from a malicious person.

There is also the string `"C:\windows\system32\kerne132.dll"` which is "kernel32" with 'l' replaced by '1'. This indicates that they might try to disguise this dll file as Windows kernel32.dll. This is because 1 and l looks similar with the normal font if we do not pay close attention.

- #### .DLL:
I found the string "127.26.152.13", which indicates that this malware may try to talk to this IP address.

### PEiD
Using PEiD showed only "Microsoft Visual C++ 6.0", so the program doesn't seem to be packed.  

### PEViewer
I used PEViewer to see the values in the .rdata section, which usually contains information about imported and exported functions. 

I saw several functions relating to finding files and moving files. 

Along with the suspicious kerne132.dll string, this suggests that this malware may copy a file into system32 folder. 
Normal program will not usually copy files into system32 folder because it contains core functions of Windows. Thus, this suggests that this program has bad intention. 

### Dependency Walker
Using DependencyWalker on the `.EXE`, I saw 2 imported functions: `CreateProcess` and `Sleep`. 

According to the sample answer of this lab, the `Practical Malware Analysis` textbook teaches us that these functions can be combined to create a backdoor for running this malware.

---
# Lab 1-2

## Executive Summary
From my analysis, this malware seems to make internet access to an obfuscated URL whose name contain a string related to InternetExplorer.

I also found that the malware seems to be finding the virutal memory of another process, changing its access permission, and modify it. 

However, to identify its actual behaviour, I need more analysis. 

## Indicators of Compromise
**Compilation Date (according to VirusTotal):**  2011-01-19 16:10:41 UTC 

**MD5 Hash of the file:**  8363436878404da0ae3e46991e355b83 

**URL of Network Connection to look for:** URL that has words similar to "Internet Explorer".

## Mitigations
- Remove the file with the hash.
- Keep track of the network logs for accesses to URLs with words similar to InternetExplorer. Then, we can identify the potential malicious proccess.  

## Evidence
I examined lab01-02.exe with the following tool. 

### VirusTotal
The program was flagged by 53/70 security vendors flagged this as malicious. 

### strings
I saw the string "MalService". This suggests that it's trying to access mail service. 

I also saw multiple strings that can combine into "http://wwareanysisbook.coom#Int6netExplo!r 8FEI.0<". This seems to be an URL relating to InternetExplorer. The link is broken and it looks suspicious as normal programs do not have broken links. 

### PEiD
Using PEiD did not show any packer, so the program doesn't seem to be packed.  

### PEViewer

Using the PEViewer, I saw the program use the
following dll:
- ADVAPI32.dll: This suggests that the program uses registry.  
- WININET.dll: This suggests that the program connects to the Internet. 

Then, I saw the following functions used:
- InternetOpenA: According to Windows API, this is a function to initialize the use of WININET.dll. This means that the program does use the library. Along with the weird URL seen earlier, this suggests that this program accesses an URL that is obfuscated, which is typical of a malware as normal and legitimate programs have no need to do this. 
- VirtualProtect, VirtualAlloc, GetProcAddress, and VirtualFree: According to Windows API, these are functions to change the access permission to the virtual memory of other processes and manipulate the memory. This can be used by this program to gain access to the memory of other programs, which could be dangerous. This suggests that this could be malicious.

### Dependency Walker 
The result of Dependency Walker only shows us the libraries and functions seen in PEViewer, so no new information was found.

---
# Lab 1-3

## Executive Summary
I found that the program is packed, so this suggests that this program could be malicious. 

I would need to unpack and do further analysis to understand this program. 

## Indicators of Compromise
**Compilation Date (according to VirusTotal):**   2011-03-26 06:54:39 UTC 

**MD5 Hash of the file:**  9c5c27494c28ed0b14853b346b113145

## Mitigations
- Remove the file with the hash.

## Evidence
I examined lab01-03.exe with the following tool. 

### VirusTotal
61/70 security vendors flagged this as malicious. 

### strings
Running strings only show us little readable strings, the 2 most important ones are:
- LoadLibraryA: 
- GetProcAddress:

According to the Windows API, the LoadLibraryA can be used to load a library dynamically and then we can use GetProcAddress to get the address of the function.  

According to the `Practical Malware Analysis` textbook, this lack of readable strings suggests that the program may be packed. 

### PEiD
Then, using PEiD, we saw that the program was indeed packed by FSG 1.0. This suggests that the program can be malicious as normal programs are not usually packed.  

### PEViewer
As the result of packing, using PEViewer does not show us any useful information. 

### Dependency Walker 
Using Dependency Walker only showed KERNEL32.dll, which can be seen with the strings tool, so no new useful information was found 

---
# Lab 1-4

## Executive Summary
This program seems to be malicious because it uses winup.exe which can be used to monitor and manipulate other running programs.

Also, the program seems to download a file from the internet. However, besides the inaccessible link, there are no other links that I saw.  

Moreover, the program seems to modify some privileges of the access token of a process. 

I need to do more analysis to identify exactly which process and which privilege it is trying to modify. 

## Indicators of Compromise
**Compilation Date (according to VirusTotal):**    2019-08-30 22:26:59 UTC 

**MD5 Hash of the file:**   625ac05fd47adc3c63700c3b30de79ab 

**Check if winup.exe is running:** If this malware is running, then winup.exe is very likely to also be running. 

## Mitigations
- Remove the file with the hash.
- Check task manager for winup.exe

## Evidence
I examined lab01-04.exe with the following tool. 

### VirusTotal
57/70 security vendors flagged this file as malicious. 

### strings
We found several notable strings: 
- winlogon.exe: According to the Wikipedia, it is a program that is responsible for the secure attention sequence (a sequence to guarantee to the user that the logon window is secured). Also, the page says that this program is a common target of threats.     
- \system32\wupdmgr.exe: According to file.net, this is a program that runs the Windows Update Manger. 
- \winup.exe: According to file.net, winup.exe is a program that can be used to monitor and manipulate other programs despite not being a Windows core program. Thus, this suggests that this program is malicious. 

We also found these strings: 
- http://www.practicalmalwareanalysis.com/updater.exe: I tried to access this file but failed because the domain no longer exists. 
- URLDownloadToFileA: According to Windows API, this function is used to download a file. 
- urlmon.dll: According to processlibrary.com, urlmon.dll is used by Object Linking and Embedding process. 

### PEiD
Using PEiD only shows "Microsoft Visual C++ 6.0", so the program does not seem to be packed. 

### PEViewer
Using PEViewer does not show any new significant information. 

### Dependency Walker 
Using Dependency Walker shows that the program uses the ADVAPI32.dll library with the following functions: 
- OpenProcessToken: According to Windows API, this is used to open the access token of a process.
- LookupPrivilegeValueA: According to Windows API, this is used to get the locally unique identifier value of a privilege name. 
- AdjustTokenPrivileges: According to Windows API, this is used to enable/disable a privilege in the access token. 

These 3 functions suggest that this program is trying to modify the privileges of the access token of some processes.
Normal programs do not usually access and modify other processes because they are usually self-contained. Thus, this program could be malicious.  

# References
- wupdmgr.exe: https://www.file.net/process/wupdmgr.exe.html
- winlogin.exe: https://en.wikipedia.org/wiki/Winlogon
- winup.exe: https://www.file.net/process/winup.exe.html
- urlmon.dll: https://www.processlibrary.com/en/directory/files/urlmon/19481/
- Object Linking and Embedding: https://www.techopedia.com/definition/4995/object-linking-and-embedding-ole


