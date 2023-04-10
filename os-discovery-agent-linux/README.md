# OS Discovery Agent For Linux

## Description

**Community** supported alternative to Intersight OS Discovery Tool that can run on baremetal hosts and populate driver information in Intersight via IPMI

gather_inventory_from_host.sh - Creates a yaml file called host-inv.yaml using most of the pre-existing inventory scripts from the intersight-python-utils/os-discovery-tool and calls send_inventory_to_imc.sh

send_inventory_to_imc.sh - Reads the host-inv.yaml created by inventory.sh and writes it to the IMC via IPMI

## Table of Contents (Optional)

- [Installation](#installation)
- [Usage](#usage)
- [Details](#details)
- [License](#license)
- [Limitations](#limitations)

## Installation

Host Package Requirements:

modinfo

lspci

lshw

ipmitool

## Usage

Provide instructions and examples for use. Include screenshots as needed.


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

The last section of a high-quality README file is the license. This lets other developers know what they can and cannot do with your project. If you need help choosing a license, refer to [https://choosealicense.com/](https://choosealicense.com/).

## Limitations

🛑 Currently limited to Ubuntu (Tested specifically on Ubuntu 22.04) and Redhat Enterprise Linux (Tested specifically on RHEL 7.9 and 8.6)

🛑 Currently no GPU support, only inventory of ethernet/fc/storage drivers

🛑 This is a COMMUNITY Supported Example (Eg. No TAC Support)
