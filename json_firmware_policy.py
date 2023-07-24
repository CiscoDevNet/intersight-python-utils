'''
Create a Firmware Policy
'''
from intersight.api import organization_api
from intersight.api import firmware_api
from intersight.model.firmware_policy import FirmwarePolicy
import credentials


if __name__ == "__main__":
    api_client = credentials.config_credentials()

    organization = organization_api.OrganizationApi(api_client).get_organization_organization_list(filter="Name eq 'Demo-DevNet'")

    # FW policy payload as a Python dictionary passed to the FirmwarePolicy model
    firmware_policy_dict = {
        "Organization": {
            "ObjectType": "organization.Organization",
            "Moid": organization.results[0].moid
        },
        "Name": "DevNet-Firmware",
        "TargetPlatform": "FIAttached",
        "ModelBundleCombo": [
            {
                "ModelFamily": "UCSB-B200-M5",
                "BundleVersion": "4.2(3d)"
            }
        ]
    }
    firmware_policy = FirmwarePolicy(**firmware_policy_dict)

    firmware_policy_instance = firmware_api.FirmwareApi(api_client)
    api_response = firmware_policy_instance.create_firmware_policy(firmware_policy)
    print("Name: %s, Model Bundle Combo %s" % (api_response.name, api_response.model_bundle_combo))
