'''
power cycle a server by its name
'''
import sys
import intersight
from intersight.api import compute_api
from intersight.model import compute_server_setting as compute
import credentials


# power cycle a server by its name
def power_cycle_server(api_client, server_name):
    # Creating the compute api instance.
    compute_instance = compute_api.ComputeApi(api_client)

    try:
        # Create a compute.ServerSetting resource
        api_response = compute_instance.get_compute_server_setting_list(filter="Name eq '" + server_name + "'")
        if len(api_response.results) == 0:
            print("No servers found with name: " + server_name)
            sys.exit(1)
        else:
            # Power cycle the server
            api_response = compute_instance.update_compute_server_setting(api_response.results[0].moid, compute.ComputeServerSetting(admin_power_state="PowerCycle"))
            return api_response
    except intersight.ApiException as exp:
        print("Exception when calling ComputeApi-> get_compute_physical_summary_list: %s\n" % exp)
        sys.exit(1)


def main():
    api_client = credentials.config_credentials()

    server_name = "SJC07-R14-FI-1-1-4"
    power_cycle = power_cycle_server(api_client, server_name)
    print(power_cycle)


if __name__ == "__main__":
    main()
