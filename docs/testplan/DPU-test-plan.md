# Test plan for DPU Platform for Chassis

- [Introduction](#introduction)
- [CLI Test Cases](#cli-test-cases)
    - [1.1 Check fwutil show status ](#11-check-fwutil-show-status)
    - [1.2 Check midplane ip address between NPU and DPU](#12-check-midplane-ip-address-between-NPU-and-DPU)
    - [1.3 Check fan LED speed descripton and presence](#13-check-fan-LED-speed-descripton-presence)
    - 


## Introduction

This test plan is to cover test cases for DPU platform.

## CLI Test Cases

### 1.1 Check fwutil show status

#### Steps
 * Use command `fwutil show status` to get fpd status of chassis


#### Verify in
 * Switch

#### Sample Output
```
    On Switch:
        root@MtFuji-dut:/home/cisco# fwutil show status
        Chassis          Module    Component    Version          Description
        ---------------  --------  -----------  ---------------  --------------------------------
        8102-28FH-DPU-O  N/A       BIOS         4.6.gbbc979eb    BIOS - Basic Input Output System
                                   Aikido       0.8              Aikido - x86 FPGA
                                   TAM          2.7              TAM FW - x86
                                   IOFPGA       0.4              IO FPGA
                                   DPUFPGA      0.2              DPU FPGA
                                   DPUFW-0      20240208.115248  DPU-0 @ Sled0
                                   DPUFW-1      20240208.115248  DPU-1 @ Sled0
                                   DPUFW-2      20240208.115248  DPU-0 @ Sled1
                                   DPUFW-3      20240208.115248  DPU-1 @ Sled1
                                   DPUFW-4      20240208.115248  DPU-0 @ Sled2
                                   DPUFW-5      20240208.115248  DPU-1 @ Sled2
                                   DPUFW-6      20240208.115248  DPU-0 @ Sled3
                                   DPUFW-7      20240208.115248  DPU-1 @ Sled3
                                   DPUCPLD0     0.3              DPU CPLD @ Sled 0
                                   DPUCPLD1     0.3              DPU CPLD @ Sled 1
                                   DPUCPLD2     0.3              DPU CPLD @ Sled 2
                                   DPUCPLD3     0.3              DPU CPLD @ Sled 3
                                   eCPLD        0.9              Power CPLD

```
#### Pass/Fail Criteria
 * Verify output on switch to see all the versions are showing up as numbers major.minor version

### 1.2 Check midplane ip address between NPU and DPU 

#### Steps
 * Use command `show ip interface` to get ip addresses 


#### Verify in
 * Switch

#### Sample Output
```
    On Switch:
      root@sonic:/home/cisco# show ip interface
      Interface     Master    IPv4 address/mask    Admin/Oper    BGP Neighbor    Neighbor IP
      ------------  --------  -------------------  ------------  --------------  -------------
      Ethernet-BP0            18.0.202.0/31        up/up         N/A             N/A
      Ethernet-BP1            18.1.202.0/31        up/up         N/A             N/A
      Ethernet-BP2            18.2.202.0/31        up/up         N/A             N/A
      Ethernet-BP3            18.3.202.0/31        up/up         N/A             N/A
      Ethernet-BP4            18.4.202.0/31        up/up         N/A             N/A
      Ethernet-BP5            18.5.202.0/31        up/up         N/A             N/A
      Ethernet-BP6            18.6.202.0/31        up/up         N/A             N/A
      Ethernet-BP7            18.7.202.0/31        up/up         N/A             N/A
      docker0                 240.127.1.1/24       up/down       N/A             N/A
      eth0                    172.25.42.65/24      up/up         N/A             N/A
      eth1                    169.254.24.2/24      up/up         N/A             N/A
      eth2                    169.254.28.2/24      up/up         N/A             N/A
      eth3                    169.254.32.2/24      up/up         N/A             N/A
      eth4                    169.254.36.2/24      up/up         N/A             N/A
      eth5                    169.254.139.2/24     up/up         N/A             N/A
      eth6                    169.254.143.2/24     up/up         N/A             N/A
      eth7                    169.254.147.2/24     up/up         N/A             N/A
      eth8                    169.254.151.2/24     up/up         N/A             N/A
      lo                      127.0.0.1/16         up/up         N/A             N/A
      root@sonic:/home/cisco# 
```
#### Pass/Fail Criteria
 * Verify output on switch to see all 169.254.x.x networks are showing up.

### 1.3 Check fan LED speed descripton and presence

#### Steps
 * Use command `show platform fan` to get ip addresses 


#### Verify in
 * Switch
 * 
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# show platform fan
  Drawer    LED            FAN    Speed    Direction    Presence    Status          Timestamp
--------  -----  -------------  -------  -----------  ----------  --------  -----------------
     N/A    N/A      PSU0.fan0      50%          N/A     Present        OK  20230907 07:04:55
     N/A    N/A      PSU1.fan0      50%          N/A     Present        OK  20230907 07:04:55
fantray0    N/A  fantray0.fan0      52%       intake     Present        OK  20230907 07:04:55
fantray1    N/A  fantray1.fan0      52%       intake     Present        OK  20230907 07:04:55
fantray2    N/A  fantray2.fan0      52%       intake     Present        OK  20230907 07:04:55
fantray3    N/A  fantray3.fan0      52%       intake     Present        OK  20230907 07:04:55
root@sonic:/home/cisco#

```
#### Pass/Fail Criteria
 * Verfiy Presence, LED (green) and speed on the output


