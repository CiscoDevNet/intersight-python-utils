import intersight
import credentials
import intersight.api.compute_api
from csv import DictReader
import logging
import traceback


FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')

def main():
    # Get existing argument parser from credentials
    parser = credentials.Parser
    parser.description = 'Intersight script to set rack server tags from csv file'

    # Add argument for csv file name
    parser.add_argument('--csv_file', required=True, help='Path to csv file')

    # Create intersight api client instance and parse authentication arguments
    client = credentials.config_credentials()

    # Parse arguments again to retrieve csv file path
    args = parser.parse_args()
    try:
        # Get compute class instance
        api_instance = intersight.api.compute_api.ComputeApi(client)

        with open(args.csv_file, newline='') as csvfile:
            reader = DictReader(csvfile)
            for row in reader:
                # Construct tag values
                tags = []
                for tag_key in [k for k in row.keys() if k != 'serial']:
                    tags.append(dict(
                        key=tag_key,
                        value=row[tag_key]
                    ))
                # Find rack server resource by Serial
                server_query = api_instance.get_compute_rack_unit_list(
                    filter=f"Serial eq {row['serial']}"
                )
                # Update rack server tags
                server_update = api_instance.update_compute_rack_unit(
                    moid=server_query.results[0].moid, 
                    compute_rack_unit=dict(tags=tags)
                )
    except intersight.OpenApiException as e:
        logger.error("Exception when calling API: %s\n" % e)
        traceback.print_exc()

if __name__== "__main__":
    main()