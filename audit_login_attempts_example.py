import argparse
from datetime import datetime, timedelta
import logging
from pprint import pformat
import traceback
from typing import Text, Type
from time import sleep

import intersight
import credentials
from helpers import format_time, print_results_to_table
    
#* Place script specific intersight api imports here
import intersight.api.aaa_api

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def main():

    client = credentials.config_credentials()
    
    try:
        #* Start main code here
        #* Get aaa class instance
        api_instance = intersight.api.aaa_api.AaaApi(client)

        #* Find all aaa records for login attempts
        query_filter = "Event eq Login"
        #* Group results by Email and set CreateTime to the Latest login
        query_apply = "groupby((Email), aggregate(CreateTime with max as Latest))"
        #* Sort by latest login in descending order
        query_order_by = "Latest desc"

        #* Get aaa records using query parameters
        aaa_query = api_instance.get_aaa_audit_record_list(filter=query_filter, apply=query_apply, orderby=query_order_by)

        #* Print table output of results
        print_results_to_table(aaa_query.results)

    except intersight.OpenApiException as e:
        logger.error("Exception when calling API: %s\n" % e)
        traceback.print_exc()

if __name__== "__main__":
    main()