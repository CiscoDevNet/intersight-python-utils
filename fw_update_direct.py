import logging
from intersight.model.firmware_distributable_relationship import FirmwareDistributableRelationship
from intersight.model.compute_blade_relationship import ComputeBladeRelationship
from intersight.api import firmware_api
from intersight.model.firmware_upgrade_impact import FirmwareUpgradeImpact
from intersight.model.firmware_direct_download import FirmwareDirectDownload
from intersight.model.firmware_upgrade import FirmwareUpgrade
import intersight
# Example below based on Intersight codegen from UI actions
# Several Moids for resources are pre-populated
from credentials import config_credentials


def get_firmware_distributable_relationship():
    firmware_distributable = FirmwareDistributableRelationship(class_id="mo.MoRef",
                                                               moid="621505896567612d31eb0fbf",
                                                               object_type="firmware.Distributable",
                                                               link="https://www.intersight.com/api/v1/firmware/Distributables/621505896567612d31eb0fbf",
                                                               )
    return firmware_distributable


def get_compute_blade_relationship():
    compute_blade = ComputeBladeRelationship(moid="5fa5b87f6176752d37b73b26",
                                             object_type="compute.Blade",
                                             class_id="mo.MoRef",
                                             )
    return compute_blade


def create_firmware_direct_download():
    firmware_direct_download = FirmwareDirectDownload(upgradeoption="upgrade_mount_only",
                                                      object_type="firmware.DirectDownload",
                                                      class_id="firmware.DirectDownload",
                                                      )
    return firmware_direct_download


# Getting firmware_upgrade_impact using filter

def get_firmware_upgrade_impact(api_client, filter_):
    # Creating the firmware api instance.
    firmware_upgrade_impact_instance = firmware_api.FirmwareApi(api_client)

    try:
        # Create a firmware.UpgradeImpact resource
        api_response = firmware_upgrade_impact_instance.get_firmware_upgrade_impact_list(filter=filter_)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling FirmwareApi-> get_firmware_upgrade_impact_list: %s\n" % e)
        exit(1)


# Getting firmware_upgrade using filter

def get_firmware_upgrade(api_client, filter_):
    # Creating the firmware api instance.
    firmware_upgrade_instance = firmware_api.FirmwareApi(api_client)

    try:
        # Create a firmware.Upgrade resource
        api_response = firmware_upgrade_instance.get_firmware_upgrade_list(filter=filter_)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling FirmwareApi-> get_firmware_upgrade_list: %s\n" % e)
        exit(1)


# Creating firmware_upgrade_impact

def create_firmware_upgrade_impact1(api_client):
    # Creating the firmware api instance.
    firmware_upgrade_impact_instance = firmware_api.FirmwareApi(api_client)

    # Creation of firmware_upgrade_impact model instance.
    firmware_upgrade_impact = FirmwareUpgradeImpact()

    # Setting all the attributes for firmware_upgrade_impact model instance.
    firmware_upgrade_impact.distributable = get_firmware_distributable_relationship()
    firmware_upgrade_impact1 = get_compute_blade_relationship()
    firmware_upgrade_impact.server = [firmware_upgrade_impact1,
                                      ]
    try:
        # Create a firmware.UpgradeImpact resource
        api_response = firmware_upgrade_impact_instance.create_firmware_upgrade_impact(firmware_upgrade_impact)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling FirmwareApi-> create_firmware_upgrade_impact: %s\n" % e)
        exit(1)


# Creating firmware_upgrade

def create_firmware_upgrade2(api_client):
    # Creating the firmware api instance.
    firmware_upgrade_instance = firmware_api.FirmwareApi(api_client)

    # Creation of firmware_upgrade model instance.
    firmware_upgrade = FirmwareUpgrade()

    # Setting all the attributes for firmware_upgrade model instance.
    firmware_upgrade.direct_download = create_firmware_direct_download()
    firmware_upgrade.distributable = get_firmware_distributable_relationship()
    firmware_upgrade.server = get_compute_blade_relationship()
    firmware_upgrade.upgrade_type = "direct_upgrade"
    try:
        # Create a firmware.Upgrade resource
        api_response = firmware_upgrade_instance.create_firmware_upgrade(firmware_upgrade)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling FirmwareApi-> create_firmware_upgrade: %s\n" % e)
        exit(1)


if __name__ == "__main__":
    client = config_credentials()

    FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
    LOGGING_LEVEL = logging.INFO
    logging.basicConfig(format=FORMAT, level=LOGGING_LEVEL)
    logger = logging.getLogger()

    # Creating firmware_upgrade_impact
    logger.info("Creating the firmware_upgrade_impact.")
    firmware_upgrade_impact1 = create_firmware_upgrade_impact1(client)
    logger.info("firmware_upgrade_impact is created successfully.")

    # Creating firmware_upgrade
    logger.info("Creating the firmware_upgrade.")
    firmware_upgrade2 = create_firmware_upgrade2(client)
    logger.info("firmware_upgrade is created successfully.")
