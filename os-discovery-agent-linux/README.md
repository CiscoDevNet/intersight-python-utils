# OS Discovery Agent For Linux

## Description

Alternative to Intersight OS Discovery Tool that can run on the host via cron job (suggested on boot and every 12 hours) and populate driver information in Intersight for that host

## Table of Contents (Optional)

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)
- [Limitations](#limitations)

## Installation

Package Requirements:

modinfo

lspci

lshw

ipmitool

## Usage

Provide instructions and examples for use. Include screenshots as needed.


## Credits

List your collaborators, if any, with links to their GitHub profiles.


## License

The last section of a high-quality README file is the license. This lets other developers know what they can and cannot do with your project. If you need help choosing a license, refer to [https://choosealicense.com/](https://choosealicense.com/).

## Limitations

🛑 Currently limited to Ubuntu and Redhat Linux
🛑 No GPU support, only inventory of ethernet/fc/storage drivers

