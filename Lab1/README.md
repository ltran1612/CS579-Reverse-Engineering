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
- Check network for communication with `127.26.152.13`. 

## Evidence

This malware has 2 files: a lab01-01.exe and a lab01-01.dll. 

I examined the malware with the following tools:

### VirusTotal
These 2 files were flagged by 25 and 22 antivirus programs, respectively.

### strings

- #### .EXE: 

I found this string "WARNING_THIS_WILL_DESTROY_YOUR_MACHINE" indicating that it must come from a malicious person.

There is also the string `"C:\windows\system32\kerne132.dll"` which is "kernel32" with 'l' replaced by '1'. This indicates that they might try to disguise this dll file as Windows kernel32.dll. This is because 1 and l looks similar with the normal font if we do not pay close attention.

- #### .DLL:
I found the string "127.26.152.13", which indicates that this malware may try to talk to this IP address.

### PEViewer
I used PEViewer to see the values in the .rdata section, which usually contains information about imported and exported functions. 

I saw several functions relating to finding files and moving files. 

Along with the suspicious kerne132.dll string, this suggests that this malware may copy a file into system32 folder. 
Normal program will not usually copy files into system32 folder because it contains core functions of Windows. Thus, this suggests that this program has bad intention. 

### Dependency Walker
Using DependencyWalker on the `.EXE`, we can see which functions are imported from various other DLLs. Two of these which are particularly notable are `CreateProcess` and `Sleep`. 

The `Practical Malware Analysis` textbook teaches us that these functions can be combined to create a backdoor for running this malware.

---
# Lab 1-2

## Executive Summary
From my analysis, this malware seems to make internet access to an obfuscated URL whose name contain a string related to InternetExplorer.

I also found that the malware seems to be finding the virutal memory of another process, changing its access permission, and modify it. 

However, to identify its actual behaviour, I need more analysis. 

## Indicators of Compromise
**Compilation Date (according to VirusTotal):**  2011-01-19 16:10:41 UTC 

**MD5 Hash of the file:**  8363436878404da0ae3e46991e355b83 

## Mitigations
- Remove the file with the hash.

## Evidence
I examined lab01-02.exe with the following tool. 

### VirusTotal
The program was flagged by 27 antivirus programs. 

### strings
I saw the string "MalService". This suggests that it's trying to access mail service. 

I also saw multiple strings that can combine into "http://wwareanysisbook.coom#Int6netExplo!r 8FEI.0<". This seems to be an URL relating to InternetExplorer. The link is broken and it looks suspicious as normal programs do not have broken links. 

### PEViewer

Using the PEViewer, I saw the program uses the
following dll:
- ADVAPI32.dll: This suggests that the program uses registry.  
- WININET.dll: This suggests that the program connects to the Internet. 

Then, I saw the following functions used:
- InternetOpenA: According to Windows API, this is a function to initialize the use of WININET.dll. This means that the program does use the library. Along with the weird URL seen earlier, this suggests that this program accesses an URL that is obfuscated, which is typical of a malware as normal and legitimate programs have no need to do this. 
- VirtualProtect, VirtualAlloc, GetProcAddress, and VirtualFree: According to Windows API, these are functions to change the access permission to the virtual memory of other processes and manipulate the memory. This can be used by this program to gain access to the memory of other programs, which could be dangerous. This suggests that this could be a malware.

### Dependency Walker 
The result of Dependency Walker only shows us the libraries and functions seen in PEViewer. Thus, no librabries have been dynamically linked.  

---
# Lab 1-3

## Executive Summary
## Indicators of Compromise
## Mitigations
## Evidence
### VirusTotal

### strings

### PEViewer

### Dependency Walker 


---
# Lab 1-4

## Executive Summary
## Indicators of Compromise
## Mitigations
## Evidence
### VirusTotal

### strings

### PEViewer

### Dependency Walker 


