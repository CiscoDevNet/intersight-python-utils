'''
Delete a virtual drive
'''
import logging
from intersight.model.compute_storage_virtual_drive_operation import ComputeStorageVirtualDriveOperation
from intersight.model.compute_storage_virtual_drive import ComputeStorageVirtualDrive
from intersight.api import compute_api
from intersight.model.compute_server_setting import ComputeServerSetting
import intersight
import credentials


def create_compute_storage_virtual_drive():
    compute_storage_virtual_drive = ComputeStorageVirtualDrive(id="0",
                                                               object_type="compute.StorageVirtualDrive",
                                                               class_id="compute.StorageVirtualDrive",
                                                               )
    return compute_storage_virtual_drive


def create_compute_storage_virtual_drive_operation():
    compute_storage_virtual_drive_operation = ComputeStorageVirtualDriveOperation(admin_action="Delete",
                                                                                  controller_id="FMEZZ1-SAS",
                                                                                  object_type="compute.StorageVirtualDriveOperation",
                                                                                  class_id="compute.StorageVirtualDriveOperation",
                                                                                  )
    virtual_drives1 = create_compute_storage_virtual_drive()
    compute_storage_virtual_drive_operation.virtual_drives = [virtual_drives1,
                                                              ]
    return compute_storage_virtual_drive_operation


# Getting compute_server_setting using filter

def get_compute_server_setting(api_client, filter_):
    # Creating the compute api instance.
    compute_server_setting_instance = compute_api.ComputeApi(api_client)

    try:
        # Create a compute.ServerSetting resource
        api_response = compute_server_setting_instance.get_compute_server_setting_list(filter=filter_)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling ComputeApi-> get_compute_server_setting_list: %s\n" % e)
        exit(1)


# Updating compute_server_setting

def update_compute_server_setting1(api_client, managed_object):
    # Creating the compute api instance.
    compute_server_setting_instance = compute_api.ComputeApi(api_client)

    # Creation of compute_server_setting model instance.
    compute_server_setting = ComputeServerSetting()

    # Setting all the attributes for compute_server_setting model instance.
    compute_server_setting.storage_virtual_drive_operation = create_compute_storage_virtual_drive_operation()
    # Extracting moid from the managed object: compute_server_setting.
    moid = managed_object.moid

    try:
        # Create a compute.ServerSetting resource
        api_response = compute_server_setting_instance.update_compute_server_setting(moid, compute_server_setting)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling ComputeApi-> update_compute_server_setting: %s\n" % e)
        exit(1)


if __name__ == "__main__":
    api_client = credentials.config_credentials()

    FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
    LOGGING_LEVEL = logging.INFO
    logging.basicConfig(format=FORMAT, level=LOGGING_LEVEL)
    logger = logging.getLogger()

    # Updating compute_server_setting using the filter.
    logger.info("Updating the compute_server_setting using filter = filter1")

    # Please provide a valid filter to query the compute_server_setting. For Example "Name eq compute_server_setting1".
    filter1 = "Name eq 'SJC07-R14-FI-1-1-4'"
    compute_server_setting1_mo = get_compute_server_setting(api_client, filter1)

    # compute_server_setting1_mo is a list of all the results matching the filter is passed.

    # Checking the length of the result to check if query with filter1 returned any results.
    if compute_server_setting1_mo is not None and len(compute_server_setting1_mo.results) > 0:
        # Please select the correct index to delete the proper MO. By default the 0th index is selected.
        update_compute_server_setting1(api_client, compute_server_setting1_mo.results[0])
        logger.info("compute_server_setting is updated successfully.")
    else:
        raise Exception("The filter : %s, did not returned any result.\
                        Please provide a valid filter to query the result." % filter1)
