# CS S479/579 Reverse Engineering at NMSU
   
## Description

This repo holds my reports on reverse engineering malware samples from "Practical Malware Analysis" textbook. 

The malwares tested target Windows machines.  
These excercises were done in Spring 2023.

## Test Methodology

### General
The test system is an Ubuntu device that uses VirtualBox, a type-2 hypervisor, to run a virtual Windows machine with networking disabled.

We tested the malwares on this virtual machine.

### System Isolation

The purpose of the virtual machine is to test the malwares in an isolated environment so that they cannot affect the host machine. 

This will also allow us to take snapshots of the OS to quickly go back and forth between different states of the machine to make testing easier. 

### Network Isolation
The network connections capability of the virtual machine is disabled to make sure that the malwares cannot spread to other machines in the network. 

This is done by disabling all the network adapters of the virtual machine. 

### Tools Used
To be added

### Software Versions
+ Virtual Box Version 7.0.6 r155176 (Qt5.15.3)
+ Windows 10 Home (10.0.19041.2006 / x64 / en-US)
