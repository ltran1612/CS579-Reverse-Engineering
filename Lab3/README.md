# Week 3 - Running the Malware

This week, I learned how to set up a fake Internet using inetsim.
However, before setting the Internet, I had to change the malware run environment from Windows 10 to Windows XP. This was because according to the Professor, Windows 10 can block all of the malwares in this lab. 

Now, to set up the fake internet, I first created a virtual network with a DHCP server in VirtualBox. Then, I created another linux virtual machine (I chose Debian) to run inetsim. I then connect the 2 virtual machines to the created virtual network so that the Windows XP machine can communicate with the linux machine. 

Then, in the Windows XP, I added the IP address of the linux machine as the DNS server on the Windows machine so that DNS requests from the Windows machine will be resolved by the linux machine. 

---
# Lab 3-1 

## Executive Summary

## Indicators of Compromise

**Compilation Date (according to VirusTotal):** 2008-01-06 14:51:31 UTC

**MD5 Hash of the EXE file:** d537acb8f56a1ce206bc35cf8ff959c0

## Mitigations

- Delete files that match these files's hash. 

## Evidence

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

Thus, this showed us that this malware could be trying to run some programs. 

### PEiD

Using PEiD gave us "PEncrypt 3.1 Final -> junkcode", showing that this malware was packed with PEncrypt 3.1 Final.

### PEViewer 

### Dependency Walker

---
# Lab 3-2

## Executive Summary

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

### PEiD

### PEViewer 

### Dependency Walker

---
# Lab 3-3

## Executive Summary

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

### PEiD

### PEViewer 

### Dependency Walker
---
