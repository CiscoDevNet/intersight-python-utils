'''
get processor information for servers
'''
import sys
import intersight
from intersight.api import processor_api
import credentials


# get processor information from the processor_api
def get_processor_information(api_client, filter_):
    # Creating the compute api instance.
    processor_instance = processor_api.ProcessorApi(api_client)

    try:
        # Create a compute.ServerSetting resource
        api_response = processor_instance.get_processor_unit_list(filter=filter_)
        return api_response
    except intersight.ApiException as exp:
        print("Exception when calling ComputeApi-> get_compute_physical_summary_list: %s\n" % exp)
        sys.exit(1)


def main():
    api_client = credentials.config_credentials()

    filter_ = "contains(Vendor,'Intel')"
    processor_information = get_processor_information(api_client, filter_)
    print(processor_information)


if __name__ == "__main__":
    main()
