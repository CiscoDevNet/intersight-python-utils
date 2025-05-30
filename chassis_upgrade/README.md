# ChassisUpgrade

This folder contains the **Chassis Upgrade Script** for upgrading the firmware of Cisco Washington Chassis. The script is designed to update critical components, including the Power Supply Unit (PSU), ensuring your infrastructure remains secure and up-to-date.

## Features

- Automates the upgrade process for chassis firmware.
- Handles critical components such as PSU.
- Provides logging and error handling for upgrade operations.

## Usage

1. Ensure you have Python and Intersight SDK installed.
2. Update the Intersight API key ID and Secret Key path in the file before running the script.
2. Prepare your `chassisData` input. **Important:**  
    - Add the chassis serial number (`chassisSerial`).
    - Add the Chassis image version (`psuImageVersion`).

    Example:
    ```json
    {
      "chassisSerial": "ABC123XYZ",
      "psuImageVersion": "4.3(6.252629)"
    }
    ```

3. Run the upgrade script as per the instructions in the script file.

## Support

For issues or questions, please open an contact Cisco TAC.