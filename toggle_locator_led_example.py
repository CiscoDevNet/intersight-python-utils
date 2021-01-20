import argparse
from datetime import timedelta
import logging
from pprint import pformat
import traceback
from typing import Text, Type
from time import sleep

import intersight
import credentials
from helpers import format_time, print_results_to_table
#* Place script specific intersight api imports here
import intersight.api.compute_api

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def toggle_server_locator_led(client: Type[intersight.ApiClient], serial: Text) -> None:
    logger.info(f"Toggling locator led for {serial}")

    #* Get compute class instance
    api_instance = intersight.api.compute_api.ComputeApi(client)

    #* Find rack server resource by Serial
    server_query = api_instance.get_compute_rack_unit_list(filter=f"Serial eq {serial}", expand="LocatorLed")

    #* Store locator led state to a var and toggle the value
    led_state = server_query.results[0].locator_led.oper_state
    logger.info(f"Previous led state = {led_state}")
    new_state = "On" if led_state == "off" else "Off"

    #* Get server settings by Server Moid
    server_settings_query = api_instance.get_compute_server_setting_list(filter=f"Server.Moid eq '{server_query.results[0].moid}'")

    #* Update server settings with toggled led value
    update_result = api_instance.update_compute_server_setting(moid=server_settings_query.results[0].moid, compute_server_setting=dict(admin_locator_led_state=new_state))

    #* Pause for eventual consistency to catch up
    new_settings_query = api_instance.get_compute_server_setting_list(filter=f"Server.Moid eq '{server_query.results[0].moid}'", expand="LocatorLed")
    retries = 0
    while(retries <= 10 and new_settings_query.results[0].config_state.lower() == 'applying'):
        logger.info("Waiting for eventual consistency to occur...")
        sleep(2)
        #* Retrieve new led operational state
        new_settings_query = api_instance.get_compute_server_setting_list(filter=f"Server.Moid eq '{server_query.results[0].moid}'", expand="LocatorLed")
        retries += 1

    if new_settings_query.results[0].locator_led.oper_state.lower() != new_state.lower():
        logger.error("Timeout occurred waiting for eventual consistency.  Led operstate never changed")
    else:
        logger.info(f"New led state = {new_settings_query.results[0].locator_led.oper_state}")



def main():

    #* Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to toggle the locator led of a rack server by serial'

    #* Place script specific arguments here
    parser.add_argument('--serial', required=True, help='Serial number of the racks server for toggling the locator led')

    client = credentials.config_credentials()

    args = parser.parse_args()

    try:
        #* Start main code here
        #* Toggle locator led for compute rack unit with supplied serial
        toggle_server_locator_led(client, args.serial)

    except intersight.OpenApiException as e:
        logger.error("Exception when calling API: %s\n" % e)
        traceback.print_exc()

if __name__== "__main__":
    main()