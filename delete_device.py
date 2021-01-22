"""Delete an Intersight device via the Intersight API."""
import sys
import json
import traceback
import intersight.api.asset_api
import credentials


def delete_device(api_client, target_host):
    result = dict(changed=False)

    # create API instance
    api_instance = intersight.api.asset_api.AssetApi(api_client)

    kwargs = dict(filter="ConnectionStatus eq 'Connected'")
    api_result = api_instance.get_asset_device_registration_list(**kwargs)

    for device in api_result.results:
        if device.device_ip_address[0] == target_host:
            api_instance.delete_asset_device_claim(moid=device.device_claim.moid)
            print("Device deleted:", target_host)
            result['changed'] = True
            break
    else:
        # for loop completed without finding the device
        print("Device not found or not connected:", target_host)

    print(json.dumps(result))


def main():
    # * Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to delete device by IP address'

    # * Place script specific arguments here
    parser.add_argument(
        '-t',
        '--target_host',
        required=True,
        help='Target host ip to delete.  Deletes 1st device found with the specified IP(does not handle multiple devices with same IPs in an account'
    )

    api_client = credentials.config_credentials()

    args = parser.parse_args()

    try:
        # * Start main code here
        # * Delete device with specified IP
        delete_device(api_client, args.target_host)

    except intersight.OpenApiException as exp:
        print("Exception when calling API: %s\n" % exp)
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
