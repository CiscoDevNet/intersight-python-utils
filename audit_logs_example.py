import logging
from pprint import pformat
import traceback

import intersight.api.aaa_api
import credentials

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def get_audit_logs(api_client):
    """Query audit records"""
    # Create an instance of the API class
    api_instance = intersight.api.aaa_api.AaaApi(api_client)

    # Read a 'aaa.AuditRecord' resource.
    logger.info("Query audit records")
    api_response = api_instance.get_aaa_audit_record_list(
        filter="Moid ne 'bar'",
        top=10,
        skip=1,
        inlinecount="allpages",
    )
    logger.info("Audit record response: %s" % pformat(api_response))

    logger.info("Query count of audit records")
    api_response = api_instance.get_aaa_audit_record_list(
        count=True,
    )
    logger.info(pformat(api_response))


def get_audit_logs_tag_summary(api_client):
    """
    Invoke the tag summary API.
    """
    logger.info("Query tags for audit records")
    api_instance = intersight.api.aaa_api.AaaApi(api_client)
    api_response = api_instance.get_aaa_audit_record_list(
        tags='true',
    )
    logger.info(pformat(api_response))


def get_audit_log_aggregate_query(api_client):
    logger.info("Query aggregate audit records")
    api_instance = intersight.api.aaa_api.AaaApi(api_client)
    api_response = api_instance.get_aaa_audit_record_list(
        apply="groupby((UserIdOrEmail),aggregate($count as Total))",
        orderby="-Total",
    )
    logger.info(pformat(api_response.results))


def main():
    # Configure API key settings for authentication
    api_client = credentials.config_credentials()

    try:
        # Get audit log data
        get_audit_logs(api_client)
        get_audit_logs_tag_summary(api_client)
        get_audit_log_aggregate_query(api_client)

    except intersight.OpenApiException as e:
        logger.error("Exception when calling API: %s\n" % e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
