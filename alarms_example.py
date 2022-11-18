from datetime import datetime, timedelta
import logging
import traceback

import intersight
import credentials
from helpers import format_time, print_results_to_table
# Place script specific intersight api imports here
import intersight.api.cond_api


FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def main():

    client = credentials.config_credentials()

    try:
        # Start main code here
        # Get condition class instance
        api_instance = intersight.api.cond_api.CondApi(client)

        # Find all Critical severity alarms within a certain timeframe
        search_period = datetime.now() - timedelta(hours=4)
        query_filter = f"Severity eq Critical and LastTransitionTime gt {format_time(search_period)}"
        # Only include LastTransitionTime and Description in results
        query_select = "LastTransitionTime,Description"

        # Get alarms using query parameters
        alarm_query = api_instance.get_cond_alarm_list(filter=query_filter, select=query_select)

        if alarm_query.results:
            # Print table output of results ommiting uninteresting fields
            print_results_to_table(alarm_query.results, ignored_fields=['class_id', 'object_type'])
        else:
            print('No alarms found')

    except intersight.OpenApiException as e:
        logger.error("Exception when calling API: %s\n" % e)
        traceback.print_exc()


if __name__ == "__main__":
    main()
