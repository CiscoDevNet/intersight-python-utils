'''
get audit records from intersight
'''
import sys
import intersight
from intersight.api import aaa_api
import credentials


# get audit records from the audit_api
def get_audit_records(api_client, filter_):
    # Creating the audit api instance.
    audit_instance = aaa_api.AaaApi(api_client)

    try:
        # Create a audit.AuditRecord resource
        api_response = audit_instance.get_aaa_audit_record_list(filter=filter_)
        return api_response
    except intersight.ApiException as exp:
        print("Exception when calling AuditApi-> get_audit_record_list: %s\n" % exp)
        sys.exit(1)


def main():
    api_client = credentials.config_credentials()

    filter_ = "contains(Email,'dsoper')"
    audit_records = get_audit_records(api_client, filter_)
    print(audit_records)


if __name__ == "__main__":
    main()
