import logging
import traceback
import intersight
import intersight.api.server_api
import intersight.api.vnic_api
import credentials


FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def main():
    # Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to get blade MAC address information from server profile'

    # Create intersight api client instance and parse authentication arguments
    client = credentials.config_credentials()

    try:
        # Get compute class instance
        api_instance = intersight.api.server_api.ServerApi(client)

        # Get blade info
        profiles = api_instance.get_server_profile_list(filter="AssignedServer ne null")
        for profile in profiles.results:
            # print Name, Moid
            print(f"Profile name: {profile.name}, AssignedServer.Moid {profile.assigned_server.moid}, Deploy Status: {profile.deploy_status}")
            # Get blade MAC addresses
            vnic_api_instance = intersight.api.vnic_api.VnicApi(client)

            vnics = vnic_api_instance.get_vnic_eth_if_list(filter=f"Profile.Moid eq '{profile.moid}'")
            for vnic in vnics.results:
                print(f"  CDN: {vnic.cdn.value}, MAC Address: {vnic.mac_address}")


    except intersight.OpenApiException as exp:
        logger.error("Exception when calling API: %s\n" % exp)
        traceback.print_exc()


if __name__ == "__main__":
    main()
