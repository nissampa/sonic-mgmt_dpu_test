# Test plan for DPU Platform for Chassis

- [Introduction](#introduction)
- [CLI Test Cases](#cli-test-cases)
    - [1.1 Check fwutil show status ](#11-check-fwutil-show-status)
    - [1.2 Check midplane ip address between NPU and DPU](#12-check-midplane-ip-address-between-NPU-and-DPU)
    - [1.3 Check fan LED speed descripton and presence](#13-check-fan-LED-speed-descripton-and-presence)
    - [1.4 Check PSU Status](#14-check-PSU-status)
    - [1.5 Check DPU console](#15-check-dpu-console)
    - [1.6 Check platform inventory](#16-check-platform-inventory)

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
 * Use command `show platform fan` to get FAN speed and Presence

#### Verify in
 * Switch
   
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

### 1.4  Check PSU Status

#### Steps
 * Use command `show platform PSUstatus` to get PSU Status 

#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# show platform PSUstatus
PSU    Model            Serial       HW Rev      Voltage (V)    Current (A)    Power (W)  Status    LED
-----  ---------------  -----------  --------  -------------  -------------  -----------  --------  -----
PSU 1  UCSC-PSU1-2300W  DTM274202UG  A0                12.06          41.69       507.50  OK        green
PSU 2  UCSC-PSU1-2300W  DTM234505JZ  02                12.03          40.25       491.00  OK        green

```
#### Pass/Fail Criteria
 * Verfiy Status OK, LED green
   
### 1.5  Check DPU Console

#### Steps
 * Use command `dconsole_uart.py -s <0-7>` to access console for given dpu

#### Verify in
 * Switch
   
#### Sample Output
```
On Switch: (shows connection to dpu-4 console)

root@sonic:/home/cisco# dconsole_uart.py -s 4
/usr/bin/picocom -b 115200 /dev/ttyS8
picocom v3.1

port is        : /dev/ttyS8
flowcontrol    : none
baudrate is    : 115200
parity is      : none
databits are   : 8
stopbits are   : 1
escape is      : C-a
local echo is  : no
noinit is      : no
noreset is     : no
hangup is      : no
nolock is      : no
send_cmd is    : sz -vv
receive_cmd is : rz -vv -E
imap is        : 
omap is        : 
emap is        : crcrlf,delbs,
logfile is     : none
initstring     : none
exit_after is  : not set
exit is        : no

Type [C-a] [C-h] to see available commands
Terminal ready

sonic login: admin
Password: 
Linux sonic 6.1.0-11-2-arm64 #1 SMP Debian 6.1.38-4 (2023-08-08) aarch64
You are on
  ____   ___  _   _ _  ____
 / ___| / _ \| \ | (_)/ ___|
 \___ \| | | |  \| | | |
  ___) | |_| | |\  | | |___
 |____/ \___/|_| \_|_|\____|

-- Software for Open Networking in the Cloud --

Unauthorized access and/or use are prohibited.
All access and/or use are subject to monitoring.

Help:    https://sonic-net.github.io/SONiC/

Last login: Fri Jan 26 21:49:12 UTC 2024 from 169.254.143.2 on pts/1
admin@sonic:~$ 
admin@sonic:~$ 
Terminating...
Thanks for using picocom
root@sonic:/home/cisco#

```
#### Pass/Fail Criteria
 * Verfiy Login access is displayed.
 * cntrl+a and then cntrl+x to come out of the dpu console.

### 1.6  Check Platform Inventory

#### Steps
 * Use command `show platform inventory` to get inventories 

#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# show platform inventory 
    Name                Product ID      Version              Serial Number   Description

Chassis
    CHASSIS             8102-28FH-DPU-O 0.10                 FLM274802F3     Cisco 28x400G QSFPDD DPU-Enabled 2RU Smart Switch,Open SW

Route Processors
    RP0                 8102-28FH-DPU-O 0.10                 FLM274802F3     Cisco 28x400G QSFPDD DPU-Enabled 2RU Smart Switch,Open SW

Sled Cards
    SLED0               8K-DPU400-2A    0.10                 FLM2750036M     Cisco 800 2xDPU Sled AMD Elba
    SLED1               8K-DPU400-2A    0.10                 FLM2750037E     Cisco 800 2xDPU Sled AMD Elba
    SLED2               8K-DPU400-2A    0.10                 FLM27500389     Cisco 800 2xDPU Sled AMD Elba
    SLED3               8K-DPU400-2A    0.10                 FLM2750038M     Cisco 800 2xDPU Sled AMD Elba

Dpu Modules
    DPU0                DSS-MTFUJI      6.1.0-11-2-arm64     FLM2750036M     Pensando DSC
    DPU1                DSS-MTFUJI      6.1.0-11-2-arm64     FLM2750036M     Pensando DSC
    DPU2                DSS-MTFUJI      6.1.0-11-2-arm64     FLM2750037E     Pensando DSC
    DPU3                DSS-MTFUJI      6.1.0-11-2-arm64     FLM2750037E     Pensando DSC
    DPU4                DSS-MTFUJI      6.1.0-11-2-arm64     FLM27500389     Pensando DSC
    DPU5                DSS-MTFUJI      6.1.0-11-2-arm64     FLM27500389     Pensando DSC
    DPU6                DSS-MTFUJI      6.1.0-11-2-arm64     FLM2750038M     Pensando DSC
    DPU7                DSS-MTFUJI      6.1.0-11-2-arm64     FLM2750038M     Pensando DSC

Power Supplies
    psutray                                                                  
        PSU0            UCSC-PSU1-2300W A0                   DTM274202UB     UCS 230000W AC-DC High Line RSP02 Power Supply
        PSU1 -- not present

Cooling Devices
    fantray0            FAN-2RU-PI-V3   N/A                  N/A             Cisco 8000 Series 2RU Fan with Port-side Air Intake Ver 3
    fantray1            FAN-2RU-PI-V3   N/A                  N/A             Cisco 8000 Series 2RU Fan with Port-side Air Intake Ver 3
    fantray2            FAN-2RU-PI-V3   N/A                  N/A             Cisco 8000 Series 2RU Fan with Port-side Air Intake Ver 3
    fantray3            FAN-2RU-PI-V3   N/A                  N/A             Cisco 8000 Series 2RU Fan with Port-side Air Intake Ver 3

FPDs
    RP0/info.0                          0.8.0-287                            \_SB_.PC00.RP07.PXSX.INFO
    RP0/info.1                          0.4.7-122                            \_SB_.PC00.RP01.PXSX.INFO
    RP0/info.2                          0.2.1-247                            \_SB_.PC00.RP10.PXSX.INFO
    RP0/info.50.auto                    10.2.0-30                            \_SB_.PC00.RP07.PXSX.P2PF

```
#### Pass/Fail Criteria
 *  Verify  product ID,version and serial of the DPU

