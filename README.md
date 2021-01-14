# intersight-python-utils

Cisco Intersight Python SDK examples.  Examples use the SDK available at https://intersight.com/apidocs/downloads/

## Python SDK Install
- Download the Python SDK from https://intersight.com/apidocs/downloads/ (be sure to dowload the OpenAPI schema version 3 SDK).  A web browser can be used to download, or you can download with wget or similar command line utilities (update the URL as needed based on the current SDK from https://intersight.com/apidocs/downloads/ :
```
wget https://cdn.intersight.com/components/an-apidocs/1.0.9-2908/model/intersight_python_sdk_v3_1.0.9.2908.tar.gz
```

- Install the SDK:
```
sudo pip install intersight_python_sdk_v3_1.0.9.2908.tar.gz
```

- Ensure that you only have one Intersight SDK active (older Intersight SDKs may conflict):
```
$ pip list
Package            Version   
------------------ ----------
<snip>
Intersight-OpenAPI 1.0.9.2908
```
(pip uninstall any intersight SDKs that may have been previously installed)

## Usage
Example scripts take API key arguments on the command line.  Here's example usage with v3 API keys:
```
python example.py --api-key-id 596cc79e5d91b400010d15ad/5db71f977564612d30cc3860/5e9217a57564612d302f475b --api-key-file=/Users/dsoper/Downloads/TME-Demo_dsoper_v3_SecretKey.txt
```
Example scripts are currently verbose in output to aid in debugging any key or authentication issues.
