from csv import DictWriter
import logging
import traceback
import intersight
import intersight.api.compute_api
import credentials


FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def main():
    # Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to get blade slot info'

    # Add argument for csv file name
    parser.add_argument('--csv_file', required=True, help='Path to csv file')

    # Create intersight api client instance and parse authentication arguments
    client = credentials.config_credentials()

    # Parse arguments again to retrieve csv file path
    args = parser.parse_args()
    try:
        # Get compute class instance
        api_instance = intersight.api.compute_api.ComputeApi(client)

        with open(args.csv_file, 'w', newline='') as csvfile:
            fieldnames = ['Chassis', 'Slot', 'OperState']
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # Get chassis info
            blades = api_instance.get_compute_blade_list(select='EquipmentChassis,SlotId', expand='EquipmentChassis($select=Name,OperState)')
            for blade in blades.results:
                writer.writerow({
                    'Chassis': blade.equipment_chassis.name,
                    'Slot': blade.slot_id,
                    'OperState': blade.equipment_chassis.oper_state
                })

    except intersight.OpenApiException as exp:
        logger.error("Exception when calling API: %s\n" % exp)
        traceback.print_exc()


if __name__ == "__main__":
    main()
