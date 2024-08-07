# OS Discovery Agent For Linux

## Description

**Community** supported alternative to Intersight OS Discovery Tool that can run on baremetal hosts and populate driver information in Intersight via IPMI.  This tool does **NOT** require any additional connectiivty or remote access unlike the original OS Disovery tool and behaves similar to ESXi ucs-tools.

_gather_inventory_from_host.sh_ - Creates a yaml file called host-inv.yaml using most of the pre-existing inventory scripts from the intersight-python-utils/os-discovery-tool and calls send_inventory_to_imc.sh

_send_inventory_to_imc.sh_  - Reads the host-inv.yaml created by gather_inventory_from_host.sh and writes it to the IMC via IPMI

![Example Image](Readme-example.png)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Details](#details)
- [License](#license)
- [Limitations](#limitations)

## Installation
**System Requirements:**
Redhat Enterprise Linux, Ubuntu

Privileged account on host that can issue ipmi commands and retrieve local inventory


**Host Software Requirements:**

modinfo, lspci, lshw, ipmitool


Note: Python is not required for this example


## Usage

Confirm all pre-requisite packages are installed

Confirm all shell scripts from repository have execute permissions

With a privileged user account run gather_inventory_from_host.sh or setup a cron job to run at boot and preferably every 24 hours

Check Host HCL status in Intersight to see populate OS & driver info

## Details

Example host-inv.yaml structure:
```
annotations:
 -kv:
  key: os.updateTimestamp
  value: 2023-04-09T20:42:58-0400
 -kv:
  key: os.kernelVersionString
  value: Red Hat Enterprise Linux 7.9
 -kv:
  key: os.releaseVersionString
  value: 3.10.0-1160.88.1.el7.x86_64
 -kv:
  key: os.type
  value: Linux
 -kv:
  key: os.vendor
  value: Red Hat
 -kv:
  key: os.name
  value: Red Hat Enterprise Linux 7.9
 -kv:
  key: os.arch
  value: x86_64
 -kv:
  key: os.driver.0.name
  value: enic
 -kv:
  key: os.driver.1.name
  value: enic
 -kv:
  key: os.driver.0.version
  value: 2.3.0.53
 -kv:
  key: os.driver.1.version
  value: 2.3.0.53
 -kv:
  key: os.driver.0.description
  value: Cisco Systems Inc VIC 1440 Mezzanine Ethernet NIC
 -kv:
  key: os.driver.1.description
  value: Cisco Systems Inc VIC 1440 Mezzanine Ethernet NIC
 -kv:
  key: os.driver.2.name
  value: fnic
 -kv:
  key: os.driver.2.version
  value: 2.0.0.89-243.0
 -kv:
  key: os.driver.2.description
  value: Cisco MQ FNIC FC
 -kv:
  key: os.driver.3.name
  value: ahci
 -kv:
  key: os.driver.4.name
  value: megaraid_sas
 -kv:
  key: os.driver.3.version
  value: 3.0
 -kv:
  key: os.driver.4.version
  value: 07.719.02.00
 -kv:
  key: os.driver.3.description
  value: Cisco Systems Inc Device 0101
 -kv:
  key: os.driver.4.description
  value: Cisco Systems Inc Device 0124
```

IPMI Command Structure
```
Delete File - 0x36 0x77 0x03 [hex-filename]
  Example Delete host-inv.yaml - ipmitool raw 0x36 0x77 0x03 0x68 0x6f 0x73 0x74 0x2d 0x69 0x6e 0x76 0x2e 0x79 0x61 0x6d 0x6c

Open and Retrieve File Descriptor - 0x36 0x77 0x00 [hex-filename]
  Example Get host-inv.yaml file descriptor - ipmitool raw 0x36 0x77 0x00 0x68 0x6f 0x73 0x74 0x2d 0x69 0x6e 0x76 0x2e 0x79 0x61 0x6d 0x6c
  IPMI will return file descriptor eg 0x08
 
Write Data to File - 0x36 0x77 0x02 [hex-filedescriptor] [hex-payload length] [hex-litle endian starting point in file] [hex-payload]
  Example write 1's (0x31) and 2's (0x32) starting at byte 40 in the host-inv.yaml file - ipmitool raw 0x36 0x77 0x02 0x03 0x14 0x28 0x00 0x00 0x00 0x31 0x31 0x31 0x31 0x31 0x31 0x31 0x31 0x31 0x32 0x32 0x32 0x32 0x32 0x32 0x32 0x32 0x32 0x32 0x0A
  
Close File Descriptor - 0x36 0x77 0x01 [hex-filedescriptor]
  Example close file ipmitool raw 0x36 0x77 0x01 0x08
```

## License
```
<#
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
#>
```
## Limitations

🛑 Currently limited to Ubuntu (Tested specifically on Ubuntu 22.04) and Redhat Enterprise Linux (Tested specifically on RHEL 7.9 and 8.6)

🛑 Currently no GPU support, only inventory of ethernet/fc/storage drivers

🛑 This is a COMMUNITY Supported Example (Eg. No TAC Support)
