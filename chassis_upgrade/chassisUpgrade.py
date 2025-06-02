"""
@NAME: chassisUpgrade.py

@TITLE: Chassis Firmware Upgrade on PSU having Power redundancy

@REQUIREMENTS: "Intersight managed chassis inventoried and discovered on UCS-Cloud/Appliance"

@AUTHOR : Sourabh Kumar (sourabhk@cisco.com)

Copyright (c) 2025, Cisco Systems, Inc.

@DESCRIPTION: chassis firmware Upgrade on PSU having Power redundancy

"""
import argparse
import intersight
import json
import time
from intersight.api_client import ApiClient
from intersight.api import aaa_api, iam_api
from intersight import signing,rest,models
from intersight.configuration import JSON_SCHEMA_VALIDATION_KEYWORDS

print("Starting Chassis Firmware Upgrade on PSU\n")
parser = argparse.ArgumentParser(description="chassis SN and Image version as command line arguments.")
parser.add_argument("arg1", type=str, help="First argument (string)")
parser.add_argument("arg2", type=str, help="Second argument (string)")
args = parser.parse_args()
chassisSerial=args.arg1
psuImageVersion=args.arg2

print("Chassis Serial Number : {}\n".format(chassisSerial))
print("Image Bundle : {}\n".format(psuImageVersion))

SUPPORTED_MODELS = \
        [
            'UCSX-9508',
        ]
try:
    conf = intersight.Configuration(
        host="https://intersight.com",
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
except Exception as excepMess1:
    print("failed to get key and secure ID {0}".format(str(excepMess1)))

conf.disabled_client_side_validations = ",".join(JSON_SCHEMA_VALIDATION_KEYWORDS)
conf.verify_ssl = True
conf.access_token = None
api_client= intersight.ApiClient(conf)
headerParams = {}
headerParams['Accept'] = api_client.select_header_accept(['application/json'])
headerParams['Content-Type'] = api_client.select_header_content_type(['application/json'])
authSettings = ['cookieAuth', 'http_signature', 'oAuth2']

try:
    chassisParams= [("$filter", "Serial eq '{0}'".format(chassisSerial))]
    response = api_client.call_api('/api/v1/equipment/Chasses', "GET", header_params=headerParams,auth_settings=authSettings,_return_http_data_only=True, _preload_content=False,query_params=chassisParams)
    chassisJson=json.loads(response.data)
    chassisMoid=chassisJson["Results"][0]["Moid"]
    chassisModel=chassisJson["Results"][0]["Model"]
    deviceID=chassisJson["Results"][0]["DeviceMoId"]
    accountID=chassisJson["Results"][0]["AccountMoid"]
    print("Chassis Model: {} \n".format(chassisModel))
except Exception as excepMess2:
    print("failed to get chassis ID and details {0}".format(str(excepMess2)))    
try:
    imageParams=[("$filter", "Version eq '{0}'".format(psuImageVersion))]
    response = api_client.call_api('/api/v1/firmware/Distributables', "GET", header_params=headerParams,auth_settings=authSettings,_return_http_data_only=True, _preload_content=False,query_params=imageParams)
    imageJson=json.loads(response.data)
    psuImageMo=imageJson["Results"][0]["Moid"]
    afterUpgradeversion=imageJson["Results"][0]["ComponentMeta"][0]["PackedVersion"]
    psuImageName=imageJson["Results"][0]["Name"]
    print("Chassis Firmware Name: {}\n ".format(psuImageName))
except Exception as excepMess3:
    print("failed to get image distributable ID {0}".format(str(excepMess3)))


try:
    print("Upgrading to Version: {}\n".format(afterUpgradeversion))
    upgradeBody={"UpgradeType":"direct_upgrade",
                "Distributable": format(psuImageMo),
                "Chassis":{"ObjectType":"equipment.Chassis", "Moid": chassisMoid}}
    response = api_client.call_api('/api/v1/firmware/ChassisUpgrades',"POST",auth_settings=authSettings,_return_http_data_only=True, _preload_content=False,body=upgradeBody,header_params=headerParams)
    upgradeJson=json.loads(response.data)
    upgradeMoid= upgradeJson["Moid"]
    upgradeStatus= upgradeJson["Status"]
    upgradestatusMoid= upgradeJson["UpgradeStatus"]["Moid"]
except Exception as excepMess4:
    print("failed to start upgrade {0}".format(str(excepMess4)))

try:
    workflowParams=[("$filter", "WorkflowCtx.InitiatorCtx.InitiatorMoid eq '{0}'".format(upgradeMoid))]
    response = api_client.call_api('/api/v1/workflow/WorkflowInfos', "GET", header_params=headerParams,auth_settings=authSettings,_return_http_data_only=True, _preload_content=False,query_params=workflowParams)
    workflowDetail=json.loads(response.data)
    workflowMoid = workflowDetail["Results"][0]["Moid"]
    traceId = workflowDetail["Results"][0]["TraceId"]
    print("Workflow ID: {} \n".format(workflowMoid))
    print("Trace ID: {} \n".format(traceId))
except Exception as excepMess5:
    print("failed to get workflow details {0}".format(str(excepMess5)))

try:
    print("Please wait for 30-40 minutes, Chassis Upgrade in Progress \n")
    workflowStatus=workflowDetail["Results"][0]["Status"]
    while (workflowStatus == "RUNNING"):
        time.sleep (180)
        response = api_client.call_api('/api/v1/workflow/WorkflowInfos', "GET", header_params=headerParams,auth_settings=authSettings,_return_http_data_only=True, _preload_content=False,query_params=workflowParams)
        workflowDetail=json.loads(response.data)
        workflowStatus=workflowDetail["Results"][0]["Status"]
        print("Upgrade is Running")
        pass
        continue
        
except Exception as excepMess6:
    print("failed at workflow upgrade status monitor {0}".format(str(excepMess6)))

try:
    time.sleep(30)
    print ("workflow status after Chassis Upgrade: {}\n".format(workflowStatus))
    response = api_client.call_api('/api/v1/workflow/WorkflowInfos', "GET", header_params=headerParams,auth_settings=authSettings,_return_http_data_only=True, _preload_content=False,query_params=workflowParams)
    workflowDetail=json.loads(response.data)
    workflowStatus=workflowDetail["Results"][0]["Status"]
    if (workflowStatus == "COMPLETED" ):
        print("Completed Upgrading to Version: {}\n".format(afterUpgradeversion))

    print("!!!! Chassis Upgrade is successfully completed on PSU !!!!\n")
except Exception as excepMess7:
    print("failed to get upgrade status {0}".format(str(excepMess7)))
