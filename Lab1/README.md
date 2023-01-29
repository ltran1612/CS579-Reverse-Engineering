# Week 1 - Simple Static Analysis

---
# Lab 1-1 

## Executive Summary
Lab01-01.exe and Lab01-01.dll seem to be a type of malware that can create a backdoor. 

It also seems to copy a file to the system32 folder and disguise that file as kernel32.dll. 

It also seems to communicate with the IP address "127.26.152.13".

However, to study the effect of the malware, we need more analysis. 

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

We examined the malware with the following tools:

### VirusTotal
These 2 files were flagged by 25 and 22 antivirus programs, respectively. (As of Jannuary 29, 2023)

### strings

#### .EXE: 

We found this string "WARNING_THIS_WILL_DESTROY_YOUR_MACHINE" indicating that it must come from a malicious person.

There is also the string `"C:\windows\system32\kerne132.dll"` which is "kernel32" with 'l' replaced by '1'. This indicates that they might try to disguise this dll file as Windows kernel32.dll. This is because 1 and l looks similar with the normal font if we do not pay close attention.

#### .DLL:
We found the string "127.26.152.13", which indicates that this malware may try to talk to this IP address.

### PEViewer
We used PEViewer to see the values in the .rdata section, which usually contains information about imported and exported functions. 

We saw several functions relating to finding files and moving files. 

Along with the suspicious kerne132.dll string, this suggests that this malware may copy a file into system32 folder. 
Normal program will not usually copy files into system32 folder because it contains core functions of Windows. Thus, this suggests that this program has bad intention. 

### Dependancy Walker
Using DependencyWalker on the `.EXE`, we can see which functions are imported from various other DLLs. Two of these which are particularly notable are `CreateProcess` and `Sleep`. 

The `Practical Malware Analysis` textbook teaches us that these functions can be combined to create a backdoor for running this malware.

---
# Lab 1-2

## Executive Summary
## Indicators of Compromise
## Mitigations
## Evidence

---
# Lab 1-3

## Executive Summary
## Indicators of Compromise
## Mitigations
## Evidence

---
# Lab 1-4

## Executive Summary
## Indicators of Compromise
## Mitigations
## Evidence

