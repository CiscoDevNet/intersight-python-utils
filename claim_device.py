"""Intersight Device Connector API configuration and device claim via the Intersight API."""
import sys
import os.path
import json
import traceback
from time import sleep
import intersight.api.asset_api
import intersight.model.asset_device_claim
import credentials
import device_connector


def claim_device(api_client, device_id, claim_code):
    # create API instance
    api_instance = intersight.api.asset_api.AssetApi(api_client)
    asset_claim = intersight.model.asset_device_claim.AssetDeviceClaim(
        serial_number=device_id,
        security_token=claim_code
    )
    api_instance.create_asset_device_claim(asset_claim)

def main():
    # * Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to delete device by IP address'

    # * Place script specific arguments here
    parser.add_argument(
        '-d',
        '--devices',
        required=True,
        help='JSON file with device access information (device hostname, username, password, and proxy settings if requred)'
    )

    api_client = credentials.config_credentials()

    args = parser.parse_args()

    return_code = 0

    if os.path.isfile(args.devices):
        with open(args.devices, 'r') as devices_file:
            devices_list = json.load(devices_file)
    else:
        # Argument devices can be a JSON string instead of file.
        # JSON string input can be used with Ansible to directly pass all info on the command line.
        devices_list = json.loads(args.devices)

    # Large try and generic exception handling with many APIs in use and exceptions possible
    try:
        for device in devices_list:
            result = dict(changed=False)
            result['msg'] = "  Host: %s" % device['hostname']
            # default access mode to allow control (Read-only False) and set to a boolean value if a string
            if not device.get('read_only'):
                device['read_only'] = False
            else:
                if device['read_only'] == 'True' or device['read_only'] == 'true':
                    device['read_only'] = True
                elif device['read_only'] == 'False' or device['read_only'] == 'false':
                    device['read_only'] = False
            # create device connector object based on device type
            if device['device_type'] == 'imc' or device['device_type'] == 'ucs' or device['device_type'] == 'ucsm' or device['device_type'] == 'ucspe':
                dc_obj = device_connector.UcsDeviceConnector(device)
            elif device['device_type'] == 'hx':
                dc_obj = device_connector.HxDeviceConnector(device)
            else:
                result['msg'] += "  Unknown device_type %s" % device['device_type']
                return_code = 1
                print(json.dumps(result))
                continue

            if not dc_obj.logged_in:
                result['msg'] += "  Login error"
                return_code = 1
                print(json.dumps(result))
                continue

            ro_json = dc_obj.configure_connector()
            if not ro_json['AdminState']:
                return_code = 1
                if ro_json.get('ApiError'):
                    result['msg'] += ro_json['ApiError']
                print(json.dumps(result))
                continue

            # set access mode (ReadOnlyMode True/False) to desired state
            if (ro_json.get('ReadOnlyMode') is not None) and (ro_json['ReadOnlyMode'] != device['read_only']):
                ro_json = dc_obj.configure_access_mode(ro_json)
                if ro_json.get('ApiError'):
                    result['msg'] += ro_json['ApiError']
                    return_code = 1
                    print(json.dumps(result))
                    continue
                result['changed'] = True

            # configure proxy settings (changes reported in called function)
            ro_json = dc_obj.configure_proxy(ro_json, result)
            if ro_json.get('ApiError'):
                result['msg'] += ro_json['ApiError']
                return_code = 1
                print(json.dumps(result))
                continue

            # wait for a connection to establish before checking claim state
            for _ in range(30):
                if ro_json['ConnectionState'] != 'Connected':
                    sleep(1)
                    ro_json = dc_obj.get_status()
                else:
                    break

            result['msg'] += "  AdminState: %s" % ro_json['AdminState']
            result['msg'] += "  ConnectionState: %s" % ro_json['ConnectionState']
            result['msg'] += "  Previous claim state: %s" % ro_json['AccountOwnershipState']

            if ro_json['ConnectionState'] != 'Connected':
                return_code = 1
                result['msg'] += "  Not connected: unable to claim"
                print(json.dumps(result))
                continue

            if ro_json['AccountOwnershipState'] != 'Claimed':
                # attempt to claim
                (claim_resp, device_id, claim_code) = dc_obj.get_claim_info(ro_json)
                if claim_resp.get('ApiError'):
                    result['msg'] += claim_resp['ApiError']
                    return_code = 1
                    print(json.dumps(result))
                    continue

                result['msg'] += "  Id: %s" % device_id
                result['msg'] += "  Token: %s" % claim_code

                # Create Intersight API instance and post ID/claim code
                claim_device(api_client, device_id, claim_code)
                result['changed'] = True

            print(json.dumps(result))

            # logout of any open sessions
            dc_obj.logout()

    except Exception as err:
        print("Exception:", str(err))
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)

    finally:
        # logout of any sessions active after exception handling
        if ('dc_obj' in locals() or 'dc_obj' in globals()):
            dc_obj.logout()

    sys.exit(return_code)


if __name__ == "__main__":
    main()
