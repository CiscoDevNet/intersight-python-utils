import logging
import traceback
from time import sleep

# Place script specific intersight api imports here
from intersight.api import iam_api
from intersight.model.iam_api_key import IamApiKey

import intersight
import credentials


FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def main():

    client = credentials.config_credentials()

    try:
        # Create version 2 API key ID and Secret key
        api_key = IamApiKey()
        api_key.purpose = 'python_key_v2'
        iam_keys_instance = iam_api.IamApi(client)
        api_response = iam_keys_instance.create_iam_api_key(api_key)
        print('Private v2 Key:', api_response.private_key)
        with open('SecretKey_Python_v2.txt', 'w') as file:
            file.write(api_response.private_key)
        api_key_id = api_response.account_moid + '/' + api_response.user.moid + '/' + api_response.moid
        print('Api v2 Key Id:', api_key_id)
        with open('ApiKeyIdFile_Python_v2', 'w') as file:
            file.write(api_key_id)
        # Delete v2 key
        api_response = iam_keys_instance.delete_iam_api_key(moid=api_response.moid)

        sleep(5)
        # Create version 3 API key ID and Secret key
        api_key.purpose = 'python_key_v3'
        api_key.hash_algorithm = 'SHA256'
        api_key.key_spec = dict(curve='P256', object_type='pkix.EcdsaKeySpec', class_id='pkix.EcdsaKeySpec')
        api_key.signing_algorithm = 'Ecdsa'
        api_response = iam_keys_instance.create_iam_api_key(api_key)
        print('Private v3 Key:', api_response.private_key)
        with open('SecretKey_Python_v3.txt', 'w') as file:
            file.write(api_response.private_key)
        api_key_id = api_response.account_moid + '/' + api_response.user.moid + '/' + api_response.moid
        print('Api v3 Key Id:', api_key_id)
        with open('ApiKeyIdFile_Python_v3', 'w') as file:
            file.write(api_key_id)
        # Delete v3 key
        api_response = iam_keys_instance.delete_iam_api_key(moid=api_response.moid)

    except intersight.OpenApiException as exp:
        logger.error("Exception when calling API: %s\n", exp)
        traceback.print_exc()


if __name__ == "__main__":
    main()
