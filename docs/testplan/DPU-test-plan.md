# Test plan for DPU Platform for Chassis

- [Introduction](#introduction)
- [CLI Test Cases](#cli-test-cases)
    - [1.1 Check fwutil show status ](#11-check-fwutil-show-status)
    - [1.2 Check midplane ip address between NPU and DPU](#12-check-midplane-ip-address-between-NPU-and-DPU)
    - [1.3 Check fan LED speed descripton and presence](#13-check-fan-LED-speed-descripton-and-presence)
    - [1.4 Check psu status](#14-check-psu-status)
    - [1.5 Check dpu console](#15-check-dpu-console)
    - [1.6 Check platform inventory](#16-check-platform-inventory)
    - [1.7 Check platform voltage](#17-check-platform-voltage)
    - [1.8 Check platform current](#18-check-platform-current)
    - [1.9 Check DPU shutdown and power up individually](#19-check-DPU-shutdown-and-power-up-individually)
    - [1.10 Check removal of pcie link between npu and dpu](#110-check-removal-of-pcie-link-between-npu-and-dpu)
    - [1.11 Check graceful restart of NPU](#111-check-graceful-restart-of-npu)
    - [1.12 Check the NTP date and timezone between DPU and NPU](#112-check-the-ntp-date-and-timezone-between-dpu-and-npu)
    - [1.13 Check the Health of Switch and DPUs](#113-check-the-health-of-switch-and-dpus)
    - [1.14 Check memory on host](#114-check-memory-on-host)
    - [1.15 Check memory on DPU](#115-check-memory-on-dpu)
    - [1.16 Check reboot cause history](#116-check-reboot-cause-history)
    - [1.17 Check CPU process on DPU](#117-check-cpu-process-on-dpu)
    - [1.18 Check the DPU state after OS rerboot](#118-check-the-dpu-state-after-os-reboot)
    - [1.19 Check DPU LED status](#119-check-dpu-led-status)

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

### 1.4 Check PSU Status

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
   
### 1.5 Check DPU Console

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

### 1.6 Check Platform Inventory

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

### 1.7 Check platform voltage

#### Steps
 * Use command `show platform voltage` to get platform voltage

#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# show platform voltage
                  Sensor    Voltage    High TH    Low TH    Crit High TH    Crit Low TH    Warning          Timestamp
------------------------  ---------  ---------  --------  --------------  -------------  ---------  -----------------
                 A1V2_BB    1211 mV       1308      1092            1320           1080      False  20230619 11:31:08
                 A1V8_BB    1810 mV       1962      1638            1980           1620      False  20230619 11:31:07
                  A1V_BB    1008 mV       1090       910            1100            900      False  20230619 11:31:06
                 A1V_CPU    1001 mV       1090       910            1100            900      False  20230619 11:31:51
               A1_2V_CPU    1209 mV       1308      1092            1320           1080      False  20230619 11:31:52
               A1_8V_CPU    1803 mV       1962      1638            1980           1620      False  20230619 11:31:51
               A2_5V_CPU    2517 mV       2725      2275            2750           2250      False  20230619 11:31:52
               A3P3V_CPU    3284 mV       3597      3003            3603           2970      False  20230619 11:31:53
                 A3V3_BB    3298 mV       3597      3003            3630           2970      False  20230619 11:31:08
       GB_CORE_VIN_L1_BB   12000 mV      13800     10200           14400           9600      False  20230619 11:31:06
      GB_CORE_VOUT_L1_BB     824 mV        N/A       614             918            608      False  20230619 11:31:50
       GB_P1V8_PLLVDD_BB    1812 mV       1962      1638            1980           1620      False  20230619 11:31:11
        GB_P1V8_VDDIO_BB    1815 mV       1962      1638            1980           1620      False  20230619 11:31:11
       GB_PCIE_VDDACK_BB     755 mV        818       683             825            675      False  20230619 11:31:12
         GB_PCIE_VDDH_BB    1208 mV       1308      1092            1320           1080      False  20230619 11:31:12
                P3_3V_BB    3330 mV       3597      3003            3630           2970      False  20230619 11:31:12
                  P5V_BB    5069 mV       5450      4550            5500           4500      False  20230619 11:31:07
                P12V_CPU   12103 mV      13080     10920           13200          10800      False  20230619 11:31:54
          P12V_SLED1_VIN   12048 mV        N/A       N/A           12550          11560      False  20230619 11:31:13
          P12V_SLED2_VIN   12048 mV        N/A       N/A           12550          11560      False  20230619 11:31:13
          P12V_SLED3_VIN   12079 mV        N/A       N/A           12550          11560      False  20230619 11:31:13
          P12V_SLED4_VIN   12043 mV        N/A       N/A           12550          11560      False  20230619 11:31:13
           P12V_STBY_CPU   12103 mV      13080     10920           13200          10800      False  20230619 11:31:54
         P12V_U1_VR3_CPU   11890 mV      13800     10200           14400           9600      False  20230619 11:31:54
         P12V_U1_VR4_CPU   11890 mV        N/A       N/A             N/A            N/A      False  20230619 11:31:54
         P12V_U1_VR5_CPU   11890 mV      13800     10200           14400           9600      False  20230619 11:31:54
         TI_3V3_L_VIN_BB   12015 mV        N/A     10200           14400           9600      False  20230619 11:31:06
     TI_3V3_L_VOUT_L1_BB    3340 mV        N/A      2839            4008           2672      False  20230619 11:31:13
         TI_3V3_R_VIN_BB   12078 mV        N/A     10200           14400           9600      False  20230619 11:31:06
     TI_3V3_R_VOUT_L1_BB    3340 mV        N/A      2839            4008           2672      False  20230619 11:31:13
   TI_GB_VDDA_VOUT_L2_BB     960 mV        N/A       816            1152            768      False  20230619 11:31:13
      TI_GB_VDDCK_VIN_BB   12031 mV        N/A     10200           14400           9600      False  20230619 11:31:06
  TI_GB_VDDCK_VOUT_L1_BB    1150 mV        N/A       978            1380            920      False  20230619 11:31:13
       TI_GB_VDDS_VIN_BB   12046 mV        N/A     10200           14400           9600      False  20230619 11:31:50
   TI_GB_VDDS_VOUT_L1_BB     750 mV        N/A       638             900            600      False  20230619 11:31:12
     VP0P6_DDR0_VTT_DPU0     599 mV        630       570             642            558      False  20230619 11:31:55
     VP0P6_DDR0_VTT_DPU1     597 mV        630       570             642            558      False  20230619 11:31:56
     VP0P6_DDR0_VTT_DPU2     600 mV        630       570             642            558      False  20230619 11:31:58
     VP0P6_DDR0_VTT_DPU3     600 mV        630       570             642            558      False  20230619 11:31:59
     VP0P6_DDR0_VTT_DPU4     599 mV        630       570             642            558      False  20230619 11:32:01
     VP0P6_DDR0_VTT_DPU5     597 mV        630       570             642            558      False  20230619 11:31:02
     VP0P6_DDR0_VTT_DPU6     596 mV        630       570             642            558      False  20230619 11:31:04
     VP0P6_DDR0_VTT_DPU7     599 mV        630       570             642            558      False  20230619 11:31:05
     VP0P6_DDR1_VTT_DPU0     600 mV        630       570             642            558      False  20230619 11:31:56
     VP0P6_DDR1_VTT_DPU1     602 mV        630       570             642            558      False  20230619 11:31:57
     VP0P6_DDR1_VTT_DPU2     601 mV        630       570             642            558      False  20230619 11:31:58
     VP0P6_DDR1_VTT_DPU3     601 mV        630       570             642            558      False  20230619 11:32:00
     VP0P6_DDR1_VTT_DPU4     600 mV        630       570             642            558      False  20230619 11:31:02
     VP0P6_DDR1_VTT_DPU5     597 mV        630       570             642            558      False  20230619 11:31:03
     VP0P6_DDR1_VTT_DPU6     596 mV        630       570             642            558      False  20230619 11:31:04
     VP0P6_DDR1_VTT_DPU7     601 mV        630       570             642            558      False  20230619 11:31:06
      VP0P6_VTT_DIMM_CPU     597 mV        654       546             660            540      False  20230619 11:31:51
      VP0P8_AVDD_D6_DPU0     801 mV        840       760             856            744      False  20230619 11:31:16
  VP0P8_AVDD_D6_DPU1_ADC     806 mV        840       760             856            744      False  20230619 11:31:20
      VP0P8_AVDD_D6_DPU2     804 mV        840       760             856            744      False  20230619 11:31:25
  VP0P8_AVDD_D6_DPU3_ADC     805 mV        840       760             856            744      False  20230619 11:31:29
      VP0P8_AVDD_D6_DPU4     806 mV        840       760             856            744      False  20230619 11:31:34
  VP0P8_AVDD_D6_DPU5_ADC     801 mV        840       760             856            744      False  20230619 11:31:39
      VP0P8_AVDD_D6_DPU6     805 mV        840       760             856            744      False  20230619 11:31:44
  VP0P8_AVDD_D6_DPU7_ADC     806 mV        840       760             856            744      False  20230619 11:31:48
           VP0P8_NW_DPU0     803 mV        840       760             856            744      False  20230619 11:31:17
           VP0P8_NW_DPU1     804 mV        840       760             856            744      False  20230619 11:31:21
           VP0P8_NW_DPU2     803 mV        840       760             856            744      False  20230619 11:31:26
           VP0P8_NW_DPU3     804 mV        840       760             856            744      False  20230619 11:31:31
           VP0P8_NW_DPU4     805 mV        840       760             856            744      False  20230619 11:31:35
           VP0P8_NW_DPU5     801 mV        840       760             856            744      False  20230619 11:31:40
           VP0P8_NW_DPU6     801 mV        840       760             856            744      False  20230619 11:31:45
           VP0P8_NW_DPU7     804 mV        840       760             856            744      False  20230619 11:31:49
VP0P8_PLL_AVDD_PCIE_DPU0     802 mV        840       760             856            744      False  20230619 11:31:56
VP0P8_PLL_AVDD_PCIE_DPU1     804 mV        840       760             856            744      False  20230619 11:31:57
VP0P8_PLL_AVDD_PCIE_DPU2     801 mV        840       760             856            744      False  20230619 11:31:59
VP0P8_PLL_AVDD_PCIE_DPU3     802 mV        840       760             856            744      False  20230619 11:32:00
VP0P8_PLL_AVDD_PCIE_DPU4     804 mV        840       760             856            744      False  20230619 11:31:02
VP0P8_PLL_AVDD_PCIE_DPU5     800 mV        840       760             856            744      False  20230619 11:31:03
VP0P8_PLL_AVDD_PCIE_DPU6     799 mV        840       760             856            744      False  20230619 11:31:05
VP0P8_PLL_AVDD_PCIE_DPU7     802 mV        840       760             856            744      False  20230619 11:31:06
     VP0P9_AVDDH_D6_DPU0     906 mV        945       855             963            837      False  20230619 11:31:15
     VP0P9_AVDDH_D6_DPU1     908 mV        945       855             963            837      False  20230619 11:31:19
     VP0P9_AVDDH_D6_DPU2     907 mV        945       855             963            837      False  20230619 11:31:24
     VP0P9_AVDDH_D6_DPU3     908 mV        945       855             963            837      False  20230619 11:31:29
     VP0P9_AVDDH_D6_DPU4     910 mV        945       855             963            837      False  20230619 11:31:33
     VP0P9_AVDDH_D6_DPU5     911 mV        945       855             963            837      False  20230619 11:31:38
     VP0P9_AVDDH_D6_DPU6     908 mV        945       855             963            837      False  20230619 11:31:43
     VP0P9_AVDDH_D6_DPU7     907 mV        945       855             963            837      False  20230619 11:31:47
   VP0P9_AVDDH_PCIE_DPU0     901 mV        945       855             963            837      False  20230619 11:31:17
   VP0P9_AVDDH_PCIE_DPU1     903 mV        945       855             963            837      False  20230619 11:31:22
   VP0P9_AVDDH_PCIE_DPU2     901 mV        945       855             963            837      False  20230619 11:31:26
   VP0P9_AVDDH_PCIE_DPU3     903 mV        945       855             963            837      False  20230619 11:31:31
   VP0P9_AVDDH_PCIE_DPU4     902 mV        945       855             963            837      False  20230619 11:31:36
   VP0P9_AVDDH_PCIE_DPU5     901 mV        945       855             963            837      False  20230619 11:31:40
   VP0P9_AVDDH_PCIE_DPU6     902 mV        945       855             963            837      False  20230619 11:31:45
   VP0P9_AVDDH_PCIE_DPU7     903 mV        945       855             963            837      False  20230619 11:31:50
        VP0P75_PVDD_DPU0     752 mV        788       713             803            698      False  20230619 11:31:15
        VP0P75_PVDD_DPU1     756 mV        788       713             802            698      False  20230619 11:31:20
        VP0P75_PVDD_DPU2     756 mV        788       713             803            698      False  20230619 11:31:24
        VP0P75_PVDD_DPU3     755 mV        788       713             802            698      False  20230619 11:31:29
        VP0P75_PVDD_DPU4     756 mV        788       713             803            698      False  20230619 11:31:34
        VP0P75_PVDD_DPU5     757 mV        788       713             802            698      False  20230619 11:31:38
        VP0P75_PVDD_DPU6     756 mV        788       713             803            698      False  20230619 11:31:43
        VP0P75_PVDD_DPU7     756 mV        788       713             802            698      False  20230619 11:31:47
       VP0P75_RTVDD_DPU0     753 mV        788       713             803            698      False  20230619 11:31:14
       VP0P75_RTVDD_DPU1     755 mV        788       713             802            698      False  20230619 11:31:19
       VP0P75_RTVDD_DPU2     752 mV        788       713             803            698      False  20230619 11:31:24
       VP0P75_RTVDD_DPU3     755 mV        788       713             802            698      False  20230619 11:31:28
       VP0P75_RTVDD_DPU4     753 mV        788       713             803            698      False  20230619 11:31:33
       VP0P75_RTVDD_DPU5     757 mV        788       713             802            698      False  20230619 11:31:38
       VP0P75_RTVDD_DPU6     755 mV        788       713             803            698      False  20230619 11:31:42
       VP0P75_RTVDD_DPU7     753 mV        788       713             802            698      False  20230619 11:31:47
   VP0P82_AVDD_PCIE_DPU0     823 mV        861       779             877            763      False  20230619 11:31:18
   VP0P82_AVDD_PCIE_DPU1     823 mV        861       779             877            763      False  20230619 11:31:22
   VP0P82_AVDD_PCIE_DPU2     822 mV        861       779             877            763      False  20230619 11:31:27
   VP0P82_AVDD_PCIE_DPU3     822 mV        861       779             877            763      False  20230619 11:31:31
   VP0P82_AVDD_PCIE_DPU4     823 mV        861       779             877            763      False  20230619 11:31:36
   VP0P82_AVDD_PCIE_DPU5     820 mV        861       779             877            763      False  20230619 11:31:41
   VP0P82_AVDD_PCIE_DPU6     819 mV        861       779             877            763      False  20230619 11:31:45
   VP0P82_AVDD_PCIE_DPU7     824 mV        861       779             877            763      False  20230619 11:31:50
     VP0P85_VDD_MAC_DPU0     853 mV        893       808             910            791      False  20230619 11:31:14
     VP0P85_VDD_MAC_DPU1     854 mV        893       808             910            791      False  20230619 11:31:19
     VP0P85_VDD_MAC_DPU2     853 mV        893       808             910            791      False  20230619 11:31:23
     VP0P85_VDD_MAC_DPU3     856 mV        893       808             910            791      False  20230619 11:31:28
     VP0P85_VDD_MAC_DPU4     856 mV        893       808             910            791      False  20230619 11:31:33
     VP0P85_VDD_MAC_DPU5     856 mV        893       808             910            791      False  20230619 11:31:37
     VP0P85_VDD_MAC_DPU6     857 mV        893       808             910            791      False  20230619 11:31:42
     VP0P85_VDD_MAC_DPU7     852 mV        893       808             910            791      False  20230619 11:31:46
           VP1P0_PCH_CPU     870 mV        N/A       N/A            1242            562      False  20230619 11:31:54
         VP1P0_PCIE4_CPU    1000 mV       1070       930            1100            900      False  20230619 11:31:54
          VP1P2_DIMM_CPU    1200 mV       1284      1116            1320           1080      False  20230619 11:31:54
        VP1P2_TVDDH_DPU0    1205 mV       1260      1140            1284           1116      False  20230619 11:31:15
    VP1P2_TVDDH_DPU1_ADC    1214 mV       1268      1140            1284           1116      False  20230619 11:31:20
        VP1P2_TVDDH_DPU2    1211 mV       1260      1140            1284           1116      False  20230619 11:31:25
    VP1P2_TVDDH_DPU3_ADC    1210 mV       1268      1140            1284           1116      False  20230619 11:31:29
        VP1P2_TVDDH_DPU4    1211 mV       1260      1140            1284           1116      False  20230619 11:31:34
    VP1P2_TVDDH_DPU5_ADC    1209 mV       1268      1140            1284           1116      False  20230619 11:31:38
        VP1P2_TVDDH_DPU6    1215 mV       1260      1140            1284           1116      False  20230619 11:31:43
    VP1P2_TVDDH_DPU7_ADC    1210 mV       1268      1140            1284           1116      False  20230619 11:31:48
              VP1P05_CPU    1075 mV       1123       977            1155            945      False  20230619 11:31:54
      VP1P8_AOD_PLL_DPU0    1801 mV       1890      1710            1926           1674      False  20230619 11:31:14
      VP1P8_AOD_PLL_DPU1    1809 mV       1890      1710            1926           1674      False  20230619 11:31:18
      VP1P8_AOD_PLL_DPU2    1810 mV       1890      1710            1926           1674      False  20230619 11:31:23
      VP1P8_AOD_PLL_DPU3    1811 mV       1890      1710            1926           1674      False  20230619 11:31:28
      VP1P8_AOD_PLL_DPU4    1811 mV       1890      1710            1926           1674      False  20230619 11:31:32
      VP1P8_AOD_PLL_DPU5    1810 mV       1890      1710            1926           1674      False  20230619 11:31:37
      VP1P8_AOD_PLL_DPU6    1810 mV       1890      1710            1926           1674      False  20230619 11:31:42
      VP1P8_AOD_PLL_DPU7    1804 mV       1890      1710            1926           1674      False  20230619 11:31:46
        VP1P8_CPLD_SLED1    1800 mV       1890      1710            1926           1674      False  20230619 11:31:55
        VP1P8_CPLD_SLED2    1808 mV       1890      1710            1926           1674      False  20230619 11:31:58
        VP1P8_CPLD_SLED3    1805 mV       1890      1710            1926           1674      False  20230619 11:32:01
        VP1P8_CPLD_SLED4    1809 mV       1890      1710            1926           1674      False  20230619 11:31:04
               VP1P8_CPU    1800 mV       1962      1591            2016           1584      False  20230619 11:31:54
          VP1P8_NIC_DPU0    1803 mV       1890      1710            1926           1674      False  20230619 11:31:16
          VP1P8_NIC_DPU1    1812 mV       1890      1710            1926           1674      False  20230619 11:31:20
          VP1P8_NIC_DPU2    1797 mV       1890      1710            1926           1674      False  20230619 11:31:25
          VP1P8_NIC_DPU3    1810 mV       1890      1710            1926           1674      False  20230619 11:31:30
          VP1P8_NIC_DPU4    1804 mV       1890      1710            1926           1674      False  20230619 11:31:35
          VP1P8_NIC_DPU5    1802 mV       1890      1710            1926           1674      False  20230619 11:31:39
          VP1P8_NIC_DPU6    1808 mV       1890      1710            1926           1674      False  20230619 11:31:44
          VP1P8_NIC_DPU7    1811 mV       1890      1710            1926           1674      False  20230619 11:31:48
       VP1P8_SE_AOD_DPU0    1806 mV       1890      1710            1926           1674      False  20230619 11:31:13
       VP1P8_SE_AOD_DPU1    1811 mV       1890      1710            1926           1674      False  20230619 11:31:18
       VP1P8_SE_AOD_DPU2    1808 mV       1890      1710            1926           1674      False  20230619 11:31:23
       VP1P8_SE_AOD_DPU3    1809 mV       1890      1710            1926           1674      False  20230619 11:31:27
       VP1P8_SE_AOD_DPU4    1811 mV       1890      1710            1926           1674      False  20230619 11:31:32
       VP1P8_SE_AOD_DPU5    1813 mV       1890      1710            1926           1674      False  20230619 11:31:36
       VP1P8_SE_AOD_DPU6    1809 mV       1890      1710            1926           1674      False  20230619 11:31:41
       VP1P8_SE_AOD_DPU7    1806 mV       1890      1710            1926           1674      False  20230619 11:31:46
         VP1P8_VCCIN_CPU    1780 mV        N/A       N/A            2002           1478      False  20230619 11:31:54
     VP1P83_POD_PLL_DPU0    1799 mV       1922      1739            1959           1702      False  20230619 11:31:16
     VP1P83_POD_PLL_DPU1    1809 mV       1922      1739            1958           1702      False  20230619 11:31:21
     VP1P83_POD_PLL_DPU2    1804 mV       1922      1739            1959           1702      False  20230619 11:31:26
     VP1P83_POD_PLL_DPU3    1804 mV       1922      1739            1958           1702      False  20230619 11:31:30
     VP1P83_POD_PLL_DPU4    1808 mV       1922      1739            1959           1702      False  20230619 11:31:35
     VP1P83_POD_PLL_DPU5    1803 mV       1922      1739            1958           1702      False  20230619 11:31:39
     VP1P83_POD_PLL_DPU6    1807 mV       1922      1739            1959           1702      False  20230619 11:31:44
     VP1P83_POD_PLL_DPU7    1805 mV       1922      1739            1958           1702      False  20230619 11:31:49
      VP2P5_DDR_VPP_DPU0    2520 mV       2625      2375            2675           2325      False  20230619 11:31:17
      VP2P5_DDR_VPP_DPU1    2528 mV       2625      2375            2675           2325      False  20230619 11:31:21
      VP2P5_DDR_VPP_DPU2    2523 mV       2625      2375            2675           2325      False  20230619 11:31:26
      VP2P5_DDR_VPP_DPU3    2529 mV       2625      2375            2675           2325      False  20230619 11:31:30
      VP2P5_DDR_VPP_DPU4    2525 mV       2625      2375            2675           2325      False  20230619 11:31:35
      VP2P5_DDR_VPP_DPU5    2523 mV       2625      2375            2675           2325      False  20230619 11:31:40
      VP2P5_DDR_VPP_DPU6    2535 mV       2625      2375            2675           2325      False  20230619 11:31:45
      VP2P5_DDR_VPP_DPU7    2528 mV       2625      2375            2675           2325      False  20230619 11:31:49
          VP2P5_STBY_CPU    2519 mV       2725      2275            2750           2250      False  20230619 11:31:53
        VP3P3_CPLD_SLED1    3307 mV       3465      3135            3531           3069      False  20230619 11:31:54
        VP3P3_CPLD_SLED2    3325 mV       3465      3135            3531           3069      False  20230619 11:31:57
        VP3P3_CPLD_SLED3    3334 mV       3465      3135            3531           3069      False  20230619 11:32:00
        VP3P3_CPLD_SLED4    3327 mV       3465      3135            3531           3069      False  20230619 11:31:03
               VP3P3_CPU    3278 mV       3597      3003            3630           2970      False  20230619 11:31:11
          VP3P3_NIC_DPU0    3289 mV       3465      3135            3531           3069      False  20230619 11:31:55
      VP3P3_NIC_DPU1_ADC    3308 mV       3465      3135            3531           3069      False  20230619 11:31:56
          VP3P3_NIC_DPU2    3293 mV       3465      3135            3531           3069      False  20230619 11:31:58
      VP3P3_NIC_DPU3_ADC    3299 mV       3465      3135            3531           3069      False  20230619 11:31:59
          VP3P3_NIC_DPU4    3306 mV       3465      3135            3531           3069      False  20230619 11:32:01
      VP3P3_NIC_DPU5_ADC    3299 mV       3465      3135            3531           3069      False  20230619 11:31:02
          VP3P3_NIC_DPU6    3308 mV       3465      3135            3531           3069      False  20230619 11:31:04
      VP3P3_NIC_DPU7_ADC    3307 mV       3465      3135            3531           3069      False  20230619 11:31:05
          VP3P3_SATA_CPU    3302 mV       3597      3003            3630           2970      False  20230619 11:31:50
             VP3P3_SLED1    3301 mV       3465      3135            3531           3069      False  20230619 11:31:13
             VP3P3_SLED2    3303 mV       3465      3135            3531           3069      False  20230619 11:31:22
             VP3P3_SLED3    3318 mV       3465      3135            3531           3069      False  20230619 11:31:32
             VP3P3_SLED4    3322 mV       3465      3135            3531           3069      False  20230619 11:31:41
      VP3P3_STBY_BMC_CPU    3322 mV       3597      3003            3603           2970      False  20230619 11:31:52
          VP3P3_STBY_CPU    3322 mV       3597      3003            3603           2970      False  20230619 11:31:53
               VP5P0_CPU    5066 mV       5450      4550            5500           4500      False  20230619 11:31:11
             VP5P0_SLED1    4964 mV       5250      4750            5350           4650      False  20230619 11:31:18
             VP5P0_SLED2    4988 mV       5250      4750            5350           4650      False  20230619 11:31:27
             VP5P0_SLED3    5003 mV       5250      4750            5350           4650      False  20230619 11:31:36
             VP5P0_SLED4    5013 mV       5250      4750            5350           4650      False  20230619 11:31:46
root@sonic:/home/cisco# 

```
#### Pass/Fail Criteria
 * Verfiy warnings are all false

### 1.8 Check platform current

#### Steps
 * Use command `show platform current` to get platform current

#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# show platform current
                 Sensor    Current    High TH    Low TH    Crit High TH    Crit Low TH    Warning          Timestamp
-----------------------  ---------  ---------  --------  --------------  -------------  ---------  -----------------
 P12V_INA_VOUT_ISEN_CPU     210 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
         P12V_SLED1_IIN   11199 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:08
         P12V_SLED2_IIN   11338 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:08
         P12V_SLED3_IIN   11163 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:08
         P12V_SLED4_IIN   11338 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:08
 P12V_U1_VR3_IINSEN_CPU    6328 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
 P12V_U1_VR4_IINSEN_CPU     750 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
P12V_U1_VR5_IINSENS_CPU     398 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
     TI_3V3_L_IINSEN_BB    1017 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
    TI_3V3_L_ISEN_L1_BB    1769 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
     TI_3V3_R_IINSEN_BB     762 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
    TI_3V3_R_ISEN_L1_BB    2257 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
  TI_GB_VDDA_ISEN_L2_BB   18000 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
  TI_GB_VDDCK_IINSEN_BB    1783 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
 TI_GB_VDDCK_ISEN_L1_BB   18125 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
   TI_GB_VDDS_IINSEN_BB    5859 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
  TI_GB_VDDS_ISEN_L1_BB   18687 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
     VP1P0_PCH_ISEN_CPU     257 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
   VP1P0_PCIE4_ISEN_CPU     111 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
    VP1P2_DIMM_ISEN_CPU     773 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
        VP1P05_ISEN_CPU    2648 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
         VP1P8_ISEN_CPU     109 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
   VP1P8_VCCIN_ISEN_CPU   13578 mA        N/A       N/A             N/A            N/A      False  20230619 11:26:09
```
#### Pass/Fail Criteria
 * Verfiy warnings are all false

### 1.9 Check DPU shutdown and power up individually

#### Steps
 * Use command `dpupwr.py off <0-7>` to shut down individual dpu
 * Use command `dpupwr.py on <0-7>` to power up individual dpu
 * Use command `show platform inventory` to show dpu status

#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# dpupwr.py off 4
/sys/bus/pci/devices/0000:8d:00.0/remove: write 1
root@sonic:/home/cisco#
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
    DPU4                DSS-MTFUJI                                           Powered off
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

root@sonic:/home/cisco# dpupwr.py on 4
Power on DPU4 for 20 seconds
Power cycle DPU4 and wait 10 seconds
Rescan PCI (30 seconds)
[52281.119280] serial 0000:8f:00.1: Couldn't register serial port c000, irq 16, type 0, error -28
Hello Mt Fuji
169.254.24.1
169.254.28.1
169.254.32.1
169.254.36.1
169.254.139.1
169.254.143.1
169.254.147.1
169.254.151.1
root@sonic:/home/cisco#
```
#### Pass/Fail Criteria
 * Verfiy dpu powered off in platform inventory after dpu shut down
 * Verify dpu is showing upon platform inventory after dpu powered on

### 1.10 Check removal of pcie link between npu and dpu

#### Steps
 * Use command `echo 1 > /sys/bus/pci/devices/BUS_ID/remove` to remove pcie link between npu and one dpu
 * Use command `dpulink.sh` to assing ip address
 * Use command `echo 1 > /sys/bus/pci/rescan` to rescan pcie links

#### Verify in
 * Switch
   
#### Sample Output
```
On Switch: Showing example of one dpu pcie link

root@sonic:/home/cisco# echo 1 > /sys/bus/pci/devices/0000:1a:00.0/remove
root@sonic:/home/cisco# ping 169.254.28.1
PING 169.254.28.1 (169.254.28.1) 56(84) bytes of data.
^C
--- 169.254.28.1 ping statistics ---
2 packets transmitted, 0 received, 100% packet loss, time 1012ms

root@sonic:/home/cisco# 
root@sonic:/home/cisco# 
root@sonic:/home/cisco# echo 1 > /sys/bus/pci/rescan
root@sonic:/home/cisco# dpulink.sh
Hello Mt Fuji
169.254.24.1
169.254.28.1
169.254.32.1
169.254.36.1
169.254.139.1
169.254.143.1
169.254.147.1
169.254.151.1
root@sonic:/home/cisco# ping 169.254.28.1
PING 169.254.28.1 (169.254.28.1) 56(84) bytes of data.
64 bytes from 169.254.28.1: icmp_seq=1 ttl=64 time=0.329 ms
^C
--- 169.254.28.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.329/0.329/0.329/0.000 ms
root@sonic:/home/cisco# 

```
#### Pass/Fail Criteria
 * Verfiy ping is not going through after removing pcie link.
 * Verify ping works between dpu and npu after bringing back up the link

### 1.11 Check graceful restart of NPU

#### Steps
 * Use command `reboot` to get reboot the host
 * Wait for NPU to come up.
 * Use command `show interface status` to chece the interfaces are up

#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# reboot
.
.
.
.
root@sonic:/home/cisco# show interface status
```
#### Pass/Fail Criteria
 * Verfiy all the interface are up.

### 1.12 Check the NTP date and timezone between DPU and NPU

#### Steps
 * Use command `date` to get date and time zone on host.
 * Use command `ssh admin@169.254.x.x` to enter into required dpu.
 * Use command `date` again on dpu to show date and time zone of dpu.
   
#### Verify in
 * Switch and dpu
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# date
.
.
root@sonic:/home/cisco# ssh admin@169.254.24.1

.
.

On DPU:
root@sonic:/home/cisco# date
```
#### Pass/Fail Criteria
 * Verfiy both the date and time zone are same

### 1.13 Check the Health of Switch and DPUs

#### Steps
 * Use command `show chassis health-events` to get chassis health events. 
   
#### Verify in
 * Switch and dpu
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# show chassis health events

```
#### Pass/Fail Criteria
 * Verfiy that the output is showing only errors related to given option.

### 1.14 Check memory on host

#### Steps
 *  Use command `TOP` to show process and memory it is using
   
#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# top
```

#### Pass/Fail Criteria 
 * Verfiy the CPU within a threshold value on DPU

### 1.15 Check memory on DPU

#### Steps
 *  Use command `top` to show process and memory it is using
   
#### Verify in
 * DPU
   
#### Sample Output
```
On DPU:

root@sonic:/home/cisco# top
```

#### Pass/Fail Criteria 
 * Verfiy the memory within a threshold value on DPU

### 1.16 Check reboot cause history

#### Steps
 *  Use command `show reboot-cause history` to show reboot cause of both switch and dpu.
   
#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# show reboot-cause history
```

#### Pass/Fail Criteria 
 * Verfiy the logs from cli to see both switch and dpus reboot history.
   
### 1.17 Check CPU process on DPU

#### Steps
 *  CLI - N/A
   
#### Verify in
 * DPU
   
#### Sample Output
```
On DPU:

CLI - N/A

```

#### Pass/Fail Criteria 
 * Verfiy the RAM using pattern read/write tests

### 1.18 Check the DPU state after OS reboot

#### Steps
 *  Use command `reboot` to reboot the os.
 *  To check DPU state - CLI - N/A
   
#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# reboot
.
.
root@sonic:/home/cisco# <CLI TO CHECK DPU STATE>
```
#### Pass/Fail Criteria 
 * Verfiy all the state changes shown by cli are reflected properly such as reboot cause, pcie link failure, etc. for all dpus

### 1.19 Check DPU LED status

#### Steps
 * CLI - N/A
   
#### Verify in
 * Switch
   
#### Sample Output
```
On Switch:

root@sonic:/home/cisco# <CLI>

```
#### Pass/Fail Criteria
 * Verfiy LEDs are Green.
