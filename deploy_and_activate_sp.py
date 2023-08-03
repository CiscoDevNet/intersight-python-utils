from intersight.api import server_api
from intersight.model.server_profile import ServerProfile
from intersight.model.policy_scheduled_action import PolicyScheduledAction
import logging
import intersight
import credentials


# Getting server_profile using filter

def get_server_profile(api_client, filter_):
    # Creating the server api instance.
    server_profile_instance = server_api.ServerApi(api_client)

    try:
        # Create a server.Profile resource
        api_response = server_profile_instance.get_server_profile_list(filter=filter_)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling ServerApi-> get_server_profile_list: %s\n" % e)
        exit(1)


# Updating server_profile

def update_server_profile1(api_client, managed_object):
    # Creating the server api instance.
    server_profile_instance = server_api.ServerApi(api_client)

    # Creation of server_profile model instance.
    server_profile = ServerProfile()
    scheduled_action1 = PolicyScheduledAction()
    scheduled_action1.action = 'Deploy'
    scheduled_action2 = PolicyScheduledAction()
    scheduled_action2.action = 'Activate'
    scheduled_action2.proceed_on_reboot = True

    # Setting all the attributes for server_profile model instance.
    server_profile.scheduled_actions = [scheduled_action1, scheduled_action2]
    # Extracting moid from the managed object: server_profile.
    moid = managed_object.moid

    try:
        # Create a server.Profile resource
        api_response = server_profile_instance.update_server_profile(moid, server_profile)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling ServerApi-> update_server_profile: %s\n" % e)
        exit(1)


if __name__ == "__main__":
    api_client = credentials.config_credentials()

    FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
    LOGGING_LEVEL = logging.INFO
    logging.basicConfig(format=FORMAT, level=LOGGING_LEVEL)
    logger = logging.getLogger()

    # Please provide a valid filter to query the server_profile. For Example "Name eq server_profile1".
    filter1 = "Name eq 'SJC07-R14'"

    server_profile1_mo = get_server_profile(api_client, filter1)

    # server_profile1_mo is a list of all the results matching the filter is passed.

    # Checking the length of the result to check if query with filter1 returned any results.
    if server_profile1_mo is not None and len(server_profile1_mo.results) > 0:
        # Please select the correct index to delete the proper MO. By default the 0th index is selected.
        update_server_profile1(api_client, server_profile1_mo.results[0])
        logger.info("server_profile is updated successfully.")
    else:
        raise Exception("The filter : %s, did not returned any result.\
                        Please provide a valid filter to query the result." % filter1)
        exit(1)

