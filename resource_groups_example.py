import logging
import traceback

# Place script specific intersight api imports here
from intersight.api import resource_api
from intersight.api import asset_api

import intersight
import credentials


FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def main():

    client = credentials.config_credentials()

    try:
        # Start main code here
        resource_instance = resource_api.ResourceApi(client)
        asset_instance = asset_api.AssetApi(client)

        query_filter = "not startsWith(Name,'License')"
        api_response = resource_instance.get_resource_group_list(filter=query_filter)
        for result in api_response.results:
            print('Resource Group:', result.name, result.per_type_combined_selector[0].combined_selector)
            reg_response = asset_instance.get_asset_device_registration_list(filter=result.per_type_combined_selector[0].combined_selector)
            for reg in reg_response.results:
                print("\tHostname: %s, Platform: %s, SN: %s" % (reg.device_hostname, reg.platform_type, reg.serial))

    except intersight.OpenApiException as exp:
        logger.error("Exception when calling API: %s\n" % exp)
        traceback.print_exc()


if __name__ == "__main__":
    main()
