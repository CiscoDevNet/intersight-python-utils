import logging
import traceback
import intersight
import intersight.api.fabric_api
import credentials


FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def main():
    # Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to get fabric multicast policies'

    # Create intersight api client instance and parse authentication arguments
    client = credentials.config_credentials()

    try:
        # Get fabric class instance
        api_instance = intersight.api.fabric_api.FabricApi(client)

        # Get multicast policy info
        mcast_policies = api_instance.get_fabric_multicast_policy_list()
        for policy in mcast_policies.results:
            # print Name, Moid
            print(f"""Multicast policy name: {policy.name},
 Snooping State: {policy.snooping_state},
 Querier State/IP/Peer: {policy.querier_state}/{policy.querier_ip_address}/{policy.querier_ip_address_peer},
 Source IP Proxy: {policy.src_ip_proxy}""")


    except intersight.OpenApiException as exp:
        logger.error("Exception when calling API: %s\n" % exp)
        traceback.print_exc()


if __name__ == "__main__":
    main()
