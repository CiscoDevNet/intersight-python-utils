"""Intersight Device Connector API configuration and target claim via the Intersight API."""
import sys
import os.path
import json
import traceback
from time import sleep
import intersight.api.asset_api
import intersight.model.asset_device_claim
from intersight.api import resource_api
from intersight.model.resource_reservation import ResourceReservation
from intersight.model.mo_mo_ref import MoMoRef
sys.path.append('../')
import credentials
import device_connector


# Get resource group moids using filter
def get_resource_groups(api_client, filter_):
    # Creating the resource api instance.
    resource_instance = resource_api.ResourceApi(api_client)

    try:
        # Create a resource.Reservation resource
        api_response = resource_instance.get_resource_group_list(filter=filter_, select='Moid')
        return api_response
    except Exception as err:
        print("Intersight Exception:", str(err))
        sys.exit(1)


# Creating resource_reservation
def create_resource_reservation(api_client, rg_moid_list):
    # Creating the resource api instance.
    resource_reservation_instance = resource_api.ResourceApi(api_client)

    # Creation of resource_reservation model instance.
    resource_reservation = ResourceReservation()

    # Setting all the attributes for resource_reservation model instance.
    rg_list = []
    for group in rg_moid_list:
        rg_list.append(MoMoRef(object_type='resource.Group', moid=group))
    resource_reservation.groups = rg_list
    resource_reservation.resource_type = "asset.DeviceRegistration"
    try:
        # Create a resource.Reservation resource
        api_response = resource_reservation_instance.create_resource_reservation(resource_reservation)
        return api_response
    except Exception as err:
        print("Intersight Exception:", str(err))
        sys.exit(1)


def claim_target(api_client, device_id, claim_code, resource_groups):
    # get resource group moids
    filter_str = "Name in (" + ', '.join("'" + rg + "'" for rg in resource_groups) + ")"
    api_response = get_resource_groups(api_client, filter_=filter_str)
    rg_moid_list = []
    for group in api_response.results:
        rg_moid_list.append(group.moid)

    # post resource group reservations
    api_response = create_resource_reservation(api_client, rg_moid_list)

    # claim with device id, claim code, and resource groups
    api_instance = intersight.api.asset_api.AssetApi(api_client)
    try:
        asset_claim = intersight.model.asset_device_claim.AssetDeviceClaim(
            serial_number=device_id,
            security_token=claim_code,
            reservation=MoMoRef(object_type='resource.Reservation', moid=api_response.moid)
        )
        api_instance.create_asset_device_claim(asset_claim)
    except Exception as err:
        print("Claim failed for device %s, claim %s" % (device_id, claim_code))
        print("Intersight Exception:", str(err))
        sys.exit(1)


def main():
    # * Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to claim target'

    # * Place script specific arguments here
    parser.add_argument(
        '-t',
        '--targets',
        required=True,
        help='JSON file with target access information (hostname, username, password, and proxy settings if requred)'
    )

    api_client = credentials.config_credentials()

    args = parser.parse_args()

    return_code = 0

    if os.path.isfile(args.targets):
        with open(args.targets, 'r') as targets_file:
            targets_list = json.load(targets_file)
    else:
        # Argument targets can be a JSON string instead of file.
        # JSON string input can be used with Ansible to directly pass all info on the command line.
        targets_list = json.loads(args.targets)

    # Large try and generic exception handling with many APIs in use and exceptions possible
    try:
        for target in targets_list:
            result = dict(changed=False)
            result['msg'] = "  Host: %s" % target['hostname']
            # default access mode to allow control (Read-only False) and set to a boolean value if a string
            if not target.get('read_only'):
                target['read_only'] = False
            else:
                if target['read_only'].lower() == 'true':
                    target['read_only'] = True
                elif target['read_only'].lower() == 'false':
                    target['read_only'] = False
            # reset_dc as bool
            if not target.get('reset_dc'):
                target['reset_dc'] = False
            else:
                if target['reset_dc'].lower() == 'true':
                    target['reset_dc'] = True
                elif target['reset_dc'].lower() == 'false':
                    target['reset_dc'] = False
             # create target connector object based on target type
            if target['device_type'] == 'imc' or target['device_type'] == 'ucs' or target['device_type'] == 'ucsm' or target['device_type'] == 'ucspe':
                dc_obj = device_connector.UcsDeviceConnector(target)
            elif target['device_type'] == 'hx':
                dc_obj = device_connector.HxDeviceConnector(target)
            else:
                result['msg'] += "  Unknown device_type %s" % target['device_type']
                return_code = 1
                print(json.dumps(result))
                continue

            if not dc_obj.logged_in:
                result['msg'] += "  Login error"
                return_code = 1
                print(json.dumps(result))
                continue

            ro_json = {}
            if target['reset_dc']:
                dc_obj.reset_dc(ro_json)
                if ro_json.get('ApiError'):
                    result['msg'] += ro_json['ApiError']
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
            if (ro_json.get('ReadOnlyMode') is not None) and (ro_json['ReadOnlyMode'] != target['read_only']):
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
                if not target.get('resource_groups'):
                    # claim to default resource group
                    target['resource_groups'] = ['default']
                claim_target(api_client, device_id, claim_code, target['resource_groups'])
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
