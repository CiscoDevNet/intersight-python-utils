from intersight.api import smtp_api
from intersight.api import server_api
from intersight.model.server_profile import ServerProfile
from intersight.model.policy_abstract_policy_relationship import PolicyAbstractPolicyRelationship
import logging
import intersight
import re
import credentials


def create_policy_abstract_policy_relationship(api_client, filter_):
    smtp_policy_instance = smtp_api.SmtpApi(api_client)

    api_response = smtp_policy_instance.get_smtp_policy_list(filter=filter_)
    logger.debug(api_response)
    smtp_policy_moid = api_response.results[0].moid
    policy_abstract_policy_relationship = PolicyAbstractPolicyRelationship(moid=smtp_policy_moid,
                                                                           object_type="smtp.Policy",
                                                                           class_id="mo.MoRef",
                                                                           )
    return policy_abstract_policy_relationship


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

def update_server_profile2(api_client, managed_object, filter_):
    # Creating the server api instance.
    server_profile_instance = server_api.ServerApi(api_client)

    # Creation of server_profile model instance.
    server_profile = ServerProfile()

    # In case user wants to pass their own policy_moid use the appropriate get function to get the moid based on filter
    smtp_policy_instance = smtp_api.SmtpApi(api_client)

    api_response = smtp_policy_instance.get_smtp_policy_list(filter=filter_)
    logger.debug(api_response)
    policy_response = api_response.results[0]

    # Extracting moid from the managed object: server_profile.
    moid = managed_object.moid

    # Getting server_profile_list from extracted moid.
    server_profile_list = get_server_profile(api_client, "Moid eq '"+moid+"'")
    policy_bucket = server_profile_list.results[0].policy_bucket
    policy_bucket_dup = policy_bucket[:]

    for index, value in enumerate(policy_bucket):
        if value["object_type"] == policy_response.object_type and value["moid"] != policy_response.moid:
            del policy_bucket_dup[index]

            break    # Setting all the attributes for server_profile model instance.
    server_profile.policy_bucket = policy_bucket_dup

    try:
        # Create a server.Profile resource
        api_response = server_profile_instance.update_server_profile(moid, server_profile)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling ServerApi-> update_server_profile: %s\n" % e)
        exit(1)


# Patching the server_profile

def patch_server_profile3(api_client, managed_object, filter_):
    # Creating the server api instance.
    server_profile_instance = server_api.ServerApi(api_client)

    # Creation of server_profile model instance.
    server_profile = ServerProfile()

    # Extracting moid from the managed object: server_profile.
    moid = managed_object.moid

    # Getting server_profile_list from extracted moid.
    server_profile_list = get_server_profile(api_client, "Moid eq '"+moid+"'")
    policy_bucket = server_profile_list.results[0].policy_bucket

    # Setting all the attributes for server_profile model instance.
    server_profile1 = create_policy_abstract_policy_relationship(api_client, filter_)
    server_profile.policy_bucket = [server_profile1,
                                    ]
    if len(policy_bucket) > 0:
        server_profile.policy_bucket.extend(policy_bucket)
    try:
        # Create a server.Profile resource
        api_response = server_profile_instance.patch_server_profile(moid, server_profile)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling ServerApi-> patch_server_profile: %s\n" % e)
        exit(1)


# Updating server_profile

def update_server_profile4(api_client, managed_object):
    # Creating the server api instance.
    server_profile_instance = server_api.ServerApi(api_client)

    # Creation of server_profile model instance.
    server_profile = ServerProfile()

    # Setting all the attributes for server_profile model instance.
    server_profile.action = "ConfigChange"
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

    smtp_filter = "Name eq 'SMTP1'"

    filter1 = "Name eq 'DevNet-Standalone'"
    server_profile1_mo = get_server_profile(api_client, filter1)

    # Checking the length of the result to check if query with filter2 returned any results.
    if server_profile1_mo is not None and len(server_profile1_mo.results) > 0:
        # Please select the correct index to delete the proper MO. By default the 0th index is selected.
        update_server_profile2(api_client, server_profile1_mo.results[0], filter_=smtp_filter)
        logger.info("server_profile is updated successfully.")
    else:
        raise Exception("The filter : %s, did not returned any result.\
                        Please provide a valid filter to query the result." % filter1)
        exit(1)

    filter1 = "Name eq 'DevNet-Standalone'"
    server_profile1_mo = get_server_profile(api_client, filter1)

    # Checking the length of the result to check if query with filter3 returned any results.
    if server_profile1_mo is not None and len(server_profile1_mo.results) > 0:
        # Please select the correct index to delete the proper MO. By default the 0th index is selected.
        patch_server_profile3(api_client, server_profile1_mo.results[0], filter_=smtp_filter)
        logger.info("server_profile is updated successfully.")
    else:
        raise Exception("The filter : %s, did not returned any result.\
                        Please provide a valid filter to query the result." % filter1)
        exit(1)

    filter1 = "Name eq 'DevNet-Standalone'"
    server_profile1_mo = get_server_profile(api_client, filter1)

    # Checking the length of the result to check if query with filter4 returned any results.
    if server_profile1_mo is not None and len(server_profile1_mo.results) > 0:
        # Please select the correct index to delete the proper MO. By default the 0th index is selected.
        update_server_profile4(api_client, server_profile1_mo.results[0])
        logger.info("server_profile is updated successfully.")
    else:
        raise Exception("The filter : %s, did not returned any result.\
                        Please provide a valid filter to query the result." % filter1)
        exit(1)
