# intersight-python-utils

Cisco Intersight Python SDK examples.  Examples use the SDK available at https://intersight.com/apidocs/downloads/

## Python SDK Install
- Download the Python SDK from https://intersight.com/apidocs/downloads/ (be sure to dowload the OpenAPI schema version 3 SDK).  You can download with wget or similar command line utilities (update the URL as needed based on the current SDK from https://intersight.com/apidocs/downloads/ :
```
wget https://cdn.intersight.com/components/an-apidocs/1.0.9-3181/model/intersight_python_sdk_v3_1.0.9.3181.tar.gz
```

- Install the SDK:
```
sudo pip install intersight_python_sdk_v3_1.0.9.3181.tar.gz
```

- Ensure that you only have one Intersight SDK active (older Intersight SDKs may conflict):
```
$ pip list
Package            Version   
------------------ ----------
<snip>
Intersight-OpenAPI 1.0.9.3181
```
(pip uninstall any intersight SDKs that may have been previously installed)

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
Example scripts are currently verbose in output to aid in debugging any key or authentication issues.
