# intersight-python-utils

Cisco Intersight Python SDK examples.  Examples use the SDK available at https://intersight.com/apidocs/downloads/

## Python SDK Install
- The Intersight Python SDK is available on the Python Package Index at https://pypi.org/project/intersight/ and can be installed using pip:
```
sudo pip install intersight
```

- Ensure that you only have one Intersight SDK active (older Intersight SDKs may conflict):
```
$ pip list
Package            Version   
------------------ ----------
<snip>
intersight         1.0.9.4437
Intersight-OpenAPI 1.0.9.3181
```
(pip uninstall any intersight SDKs that may have been previously installed)
```
pip uninstall Intersight-OpenAPI
```

## Usage
Example scripts use the credentials.py module in this directory to configure API key settings.  API key information can be provided as environment variables:
```
export INTERSIGHT_API_PRIVATE_KEY=/Users/guest/Downloads/v3_SecretKey.txt
export INTERSIGHT_API_KEY_ID=596cc...
```
OR with arguments on the command line:
```
python users_example.py --api-key-id 596cc --api-key-file ~/Downloads/devSecretKey.txt --api-key-legacy
```
Example scripts are currently verbose in output to aid in debugging any key or authentication issues.  Each script will perform example operations against the Intersight API such as retrieving alarm details and displaying in tabular form:
```
python alarms_example.py
```
(example output)
```
| creation_time                    | description                                                                                                                                | moid                     |
|----------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------+--------------------------|
| 2021-08-12 19:17:41.508000+00:00 | Chassis MF-TME-IMM/chassis-1 power supply redundancy lost                                                                                  | 611573d565696e2d3332f0b8 |
| 2021-08-14 17:31:07.014000+00:00 | One or more ports with license type ETH_PORT_ACTIVATION_PKG on fabric-interconnect B are running in the grace period for more than 90 days | 6117fddb65696e2d33372de0 |
| 2021-08-20 15:38:34.025000+00:00 | Controller 1 on server 1/7 is inoperable. Reason: CIMC did not detect storage controller                                                   | 611fce5165696e2d33dcd29f |
```