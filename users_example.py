import logging
from pprint import pformat
import traceback

import intersight.api.iam_api
import credentials

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def get_users(apiClient):
    ###################################################################################
    api_instance = intersight.api.iam_api.IamApi(apiClient)
    logger.info("Query Users")
    results = api_instance.get_iam_user_list()
    logger.info("User response: %s" % pformat(results))
    logger.info("ANCESTORS: %s" % results.results[0].ancestors)

    logger.info("Query Users with expand")
    results = api_instance.get_iam_user_list(expand='Ancestors')
    logger.info("Users: {}", pformat(results))


def main():
    # Configure API key settings for authentication
    apiClient = credentials.config_credentials()

    try:
        # Get list of users
        get_users(apiClient)

    except intersight.OpenApiException as e:
        logger.error("Exception when calling API: %s\n" % e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
