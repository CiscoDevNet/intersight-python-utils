#ChassisUpgrade.py
This folder contains the Chassis Upgrade Script for upgrading the firmware of Cisco Washington Chassis. The script is designed to update critical components, including the Power Supply Unit (PSU), ensuring your infrastructure remains secure and up-to-date.

#Features
Automates the upgrade process for chassis firmware.
Handles critical components such as PSU.
Provides logging and error handling for upgrade operations.

#Usage
Ensure you have Python and Intersight SDK installed.
Update the Intersight API key ID and Secret Key path in the file before running the script.

#CLI command to be performed
python chassisUpgrade.py "ABC123XYZ" "4.3(6.252629)"

Chassis serial number (chassisSerial) and Chassis image version (psuImageVersion) as Comamnd Line Argument is to be passed along with chassissUpgrade.py Script

#Example

"chassisSerial": "ABC123XYZ",
"psuImageVersion": "4.3(6.252629)"


#Support
For issues or questions, please open an contact Cisco TAC.
