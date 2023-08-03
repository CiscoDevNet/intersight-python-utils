'''
Create a Profile with a FW Policy Attached
'''
from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
from intersight.api import server_api
from intersight.model.server_profile import ServerProfile
from intersight.model.compute_blade_relationship import ComputeBladeRelationship
from intersight.model.server_server_assign_type_slot import ServerServerAssignTypeSlot
from intersight.model.policy_abstract_policy_relationship import PolicyAbstractPolicyRelationship
from intersight.exceptions import NotFoundException
import logging
import intersight
import re
import credentials


def get_organization_organization_relationship():
    organization_organization = OrganizationOrganizationRelationship(moid="6418bfd46972652d30a596ef",
                                                                     object_type="organization.Organization",
                                                                     class_id="mo.MoRef",
                                                                     )
    return organization_organization


def get_compute_blade_relationship():
    compute_blade = ComputeBladeRelationship(moid="641c9af36176753501b70f63",
                                             object_type="compute.Blade",
                                             class_id="mo.MoRef",
                                             )
    return compute_blade


def create_server_server_assign_type_slot():
    server_server_assign_type_slot = ServerServerAssignTypeSlot(chassis_id=0,
                                                                class_id="server.ServerAssignTypeSlot",
                                                                domain_name="",
                                                                object_type="server.ServerAssignTypeSlot",
                                                                slot_id=0,
                                                                )
    return server_server_assign_type_slot


def create_policy_abstract_policy_relationship():
    # In case user want to fetch moid based on filter un-comment below line and comment subsequent line
    # firmware_policy_moid = get_firmware_policy(api_client, filter_).results[0].moid

    firmware_policy_moid = "64bedfd57068613101e8aa28"
    policy_abstract_policy_relationship = PolicyAbstractPolicyRelationship(moid=firmware_policy_moid,
                                                                           object_type="firmware.Policy",
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


# Creating server_profile

def create_server_profile1(api_client):
    # Creating the server api instance.
    server_profile_instance = server_api.ServerApi(api_client)

    # Creation of server_profile model instance.
    server_profile = ServerProfile()

    # Setting all the attributes for server_profile model instance.
    server_profile.name = "SJC07-R14"
    server_profile.organization = get_organization_organization_relationship()
    server_profile.tags = []
    server_profile.target_platform = "FIAttached"
    try:
        # Create a server.Profile resource
        api_response = server_profile_instance.create_server_profile(server_profile)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling ServerApi-> create_server_profile: %s\n" % e)
        exit(1)


# Updating server_profile

def update_server_profile2(api_client, managed_object):
    # Creating the server api instance.
    server_profile_instance = server_api.ServerApi(api_client)

    # Creation of server_profile model instance.
    server_profile = ServerProfile()

    # Setting all the attributes for server_profile model instance.
    server_profile.assigned_server = get_compute_blade_relationship()
    server_profile.server_assignment_mode = "Static"
    server_profile.server_pool = None
    server_profile.server_pre_assign_by_serial = ""
    server_profile.server_pre_assign_by_slot = create_server_server_assign_type_slot()
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


# Patching the server_profile

def patch_server_profile3(api_client, managed_object):
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
    server_profile1 = create_policy_abstract_policy_relationship()
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
    server_profile.uuid_address_type = "NONE"
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


# Updating server_profile

def update_server_profile5(api_client, managed_object):
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

    # Creating server_profile
    logger.info("Creating the server_profile.")
    server_profile1 = create_server_profile1(api_client)
    logger.info("server_profile is created successfully.")

    # Updating server_profile
    logger.info("Updating the server_profile.")
    server_profile2 = update_server_profile2(api_client, server_profile1)
    logger.info("server_profile is updated successfully.")

    # Patching server_profile
    logger.info("Patching the server_profile.")
    server_profile3 = patch_server_profile3(api_client, server_profile1)
    logger.info("server_profile is patched successfully.")

    # Updating server_profile
    logger.info("Updating the server_profile.")
    server_profile4 = update_server_profile4(api_client, server_profile1)
    logger.info("server_profile is updated successfully.")

    # Updating server_profile
    logger.info("Updating the server_profile.")
    server_profile5 = update_server_profile5(api_client, server_profile1)
    logger.info("server_profile is updated successfully.")
