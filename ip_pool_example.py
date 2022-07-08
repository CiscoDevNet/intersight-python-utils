import logging
from intersight.model.ippool_ip_v4_block import IppoolIpV4Block
from intersight.model.ippool_ip_v4_config import IppoolIpV4Config
from intersight.model.organization_organization_relationship import OrganizationOrganizationRelationship
from intersight.api import ippool_api
from intersight.model.ippool_pool import IppoolPool
import intersight
import credentials


def create_ippool_ip_v4_block():
    ippool_ip_v4_block = IppoolIpV4Block(_from="172.28.224.32",
                                         size=40,
                                         object_type="ippool.IpV4Block",
                                         class_id="ippool.IpV4Block",
                                         )
    return ippool_ip_v4_block


def create_ippool_ip_v4_config():
    ippool_ip_v4_config = IppoolIpV4Config(gateway="172.28.224.1",
                                           netmask="255.255.254.0",
                                           primary_dns="171.70.168.183",
                                           object_type="ippool.IpV4Config",
                                           class_id="ippool.IpV4Config",
                                           )
    return ippool_ip_v4_config


def get_organization_organization_relationship():
    organization_organization = OrganizationOrganizationRelationship(moid="5deea1d16972652d33ba886b",
                                                                     object_type="organization.Organization",
                                                                     class_id="mo.MoRef",
                                                                     )
    return organization_organization


# Getting ippool_pool using filter

def get_ippool_pool(api_client, filter_):
    # Creating the ippool api instance.
    ippool_pool_instance = ippool_api.IppoolApi(api_client)

    try:
        # Create a ippool.Pool resource
        api_response = ippool_pool_instance.get_ippool_pool_list(filter=filter_)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling IppoolApi-> get_ippool_pool_list: %s\n" % e)
        exit(1)


# Creating ippool_pool

def create_ippool_pool1(api_client):
    # Creating the ippool api instance.
    ippool_pool_instance = ippool_api.IppoolApi(api_client)

    # Creation of ippool_pool model instance.
    ippool_pool = IppoolPool()

    # Setting all the attributes for ippool_pool model instance.
    ippool_pool.assignment_order = "default"
    ippool_pool1 = create_ippool_ip_v4_block()
    ippool_pool.ip_v4_blocks = [ippool_pool1,
                                ]
    ippool_pool.ip_v4_config = create_ippool_ip_v4_config()
    # ippool_pool.ip_v6_blocks = []
    ippool_pool.name = "TME-SJC07-IPs"
    ippool_pool.organization = get_organization_organization_relationship()
    try:
        # Create a ippool.Pool resource
        api_response = ippool_pool_instance.create_ippool_pool(ippool_pool)
        logger.debug(api_response)
        return api_response
    except intersight.ApiException as e:
        logger.error("Exception when calling IppoolApi-> create_ippool_pool: %s\n" % e)
        exit(1)


if __name__ == "__main__":
    client = credentials.config_credentials()

    FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
    LOGGING_LEVEL = logging.INFO
    logging.basicConfig(format=FORMAT, level=LOGGING_LEVEL)
    logger = logging.getLogger()

    # Creating ippool_pool
    logger.info("Creating the ippool_pool.")
    ippool_pool1 = create_ippool_pool1(client)
    logger.info("ippool_pool is created successfully.")
