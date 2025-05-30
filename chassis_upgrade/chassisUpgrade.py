import intersight
import json
import time
from intersight.api_client import ApiClient
from intersight.api import aaa_api, iam_api
from intersight import signing,rest,models
from intersight.configuration import JSON_SCHEMA_VALIDATION_KEYWORDS
from chassisData import chassisSerial
from chassisData import psuImageVersion


conf = intersight.Configuration(
    host="https://staging.starshipcloud.com",
    signing_info=intersight.signing.HttpSigningConfiguration(
        key_id='',
        private_key_path='',
        signing_scheme = signing.SCHEME_HS2019,
        signing_algorithm = signing.ALGORITHM_ECDSA_MODE_FIPS_186_3,
        signed_headers=[signing.HEADER_REQUEST_TARGET,
                        signing.HEADER_DATE,
                        signing.HEADER_HOST,
                        signing.HEADER_DIGEST,
                        ]
    )
)
conf.disabled_client_side_validations = ",".join(JSON_SCHEMA_VALIDATION_KEYWORDS)
conf.verify_ssl = False
conf.access_token = None
api_client= intersight.ApiClient(conf)
headerParams = {}
headerParams['Accept'] = api_client.select_header_accept(['application/json'])
headerParams['Content-Type'] = api_client.select_header_content_type(['application/json'])
authSettings = ['cookieAuth', 'http_signature', 'oAuth2']
chassisParams= [("$filter", "Serial eq '{0}'".format(chassisSerial))]
response = api_client.call_api('/api/v1/equipment/Chasses', "GET", header_params=headerParams,auth_settings=authSettings,_return_http_data_only=True, _preload_content=False,query_params=chassisParams)
chassisJson=json.loads(response.data)
chassisMoid=chassisJson["Results"][0]["Moid"]
chassisModel=chassisJson["Results"][0]["Model"]
deviceID=chassisJson["Results"][0]["DeviceMoId"]
accountID=chassisJson["Results"][0]["AccountMoid"]
print("Chassis Serial Number: {} \n".format(chassisSerial))
print("Chassis Model: {} \n".format(chassisModel))
print("Chassis ID: {} \n".format(chassisMoid))
imageParams=[("$filter", "Version eq '{0}'".format(psuImageVersion))]
response = api_client.call_api('/api/v1/firmware/Distributables', "GET", header_params=headerParams,auth_settings=authSettings,_return_http_data_only=True, _preload_content=False,query_params=imageParams)
imageJson=json.loads(response.data)
psuImageMo=imageJson["Results"][0]["Moid"]
afterUpgradeversion=imageJson["Results"][0]["ComponentMeta"][0]["PackedVersion"]
psuImageName=imageJson["Results"][0]["Name"]
print("Chassis Image Name: {}\n ".format(psuImageName))
print("Upgrading Chassis PSU to Version: {}\n".format(afterUpgradeversion))

upgradeBody={"UpgradeType":"direct_upgrade",
             "Distributable": format(psuImageMo),
             "Chassis":{"ObjectType":"equipment.Chassis", "Moid": chassisMoid}}
response = api_client.call_api('/api/v1/firmware/ChassisUpgrades',"POST",auth_settings=authSettings,body=upgradeBody,header_params=headerParams)

print("Chassis Upgrade is in Progress\n")
time.sleep(60)
print("Checking the firmware upgrade status of Chassis\n")
time.sleep(2400)
print("Completed Chassis PSU Upgrade to Version: {}\n".format(afterUpgradeversion))
print("Chassis firmware has been upgraded successfully")
