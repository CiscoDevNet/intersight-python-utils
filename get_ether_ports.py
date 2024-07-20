from csv import DictWriter
import logging
import traceback
import intersight
import intersight.api.ether_api
import credentials


FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def main():
    # Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to get ethernet ports'

    # Add argument for csv file name
    parser.add_argument('--csv_file', required=True, help='Path to csv file')

    # Create intersight api client instance and parse authentication arguments
    client = credentials.config_credentials()

    # Parse arguments again to retrieve csv file path
    args = parser.parse_args()
    try:
        # Get ether port class instance
        api_instance = intersight.api.ether_api.EtherApi(client)

        with open(args.csv_file, 'w', newline='') as csvfile:
            fieldnames = ['Dn', 'AdminState', 'OperState', 'OperStateQual']
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # Get ethernet ports
            ether_ports = api_instance.get_ether_physical_port_list(select='Dn,AdminState,OperState,OperStateQual', filter="AdminState ne 'Enabled'")
            for port in ether_ports.results:
                writer.writerow({
                    'Dn': port.dn,
                    'AdminState': port.admin_state,
                    'OperState': port.oper_state,
                    'OperStateQual': port.oper_state_qual
                })

    except intersight.OpenApiException as exp:
        logger.error("Exception when calling API: %s\n" % exp)
        traceback.print_exc()


if __name__ == "__main__":
    main()
