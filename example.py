import argparse
import datetime
import logging
from pprint import pformat
import traceback

import intersight
import intersight.api.iam_api

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def get_users(apiClient):
  ###################################################################################
  api_instance = intersight.api.iam_api.IamApi(apiClient)
  logger.info("Query Users")
  results = api_instance.get_iam_user_list()
  logger.info("User response: %s" % pformat(results))
  logger.info("ANCESTORS: %s" % results.results[0].ancestors)

  logger.info("Query Users with expand")
  results = api_instance.get_iam_user_list(expand='Ancestors')
  logger.info("Users: {}", pformat(results))


def main():
  parser = argparse.ArgumentParser(description='Intersight Python SDK test')
  parser.add_argument('--url', default='https://intersight.com',
                      help='The Intersight root URL for the API endpoint. The default is https://intersight.com')
  parser.add_argument('--ignore-tls', action='store_true', help='Ignore TLS server-side certificate verification')
  parser.add_argument('--api-key-legacy', action='store_true', help='Legacy API client key')
  parser.add_argument('--api-key-id', help='API client key id for the HTTP signature scheme')
  parser.add_argument('--api-key-file', help='Name of file containing secret key for the HTTP signature scheme')

  args = parser.parse_args()

  configuration = None
  if args.api_key_file:
    # HTTP signature scheme.
    logger.info("Using HTTP signature authentication")
    signing_scheme = intersight.signing.SCHEME_HS2019
    signing_algorithm = intersight.signing.ALGORITHM_ECDSA_MODE_FIPS_186_3
    if args.api_key_legacy:
      signing_scheme = intersight.signing.SCHEME_RSA_SHA256
      signing_algorithm = intersight.signing.ALGORITHM_RSASSA_PKCS1v15

    configuration = intersight.Configuration(
            host=args.url,
            signing_info = intersight.HttpSigningConfiguration(
                key_id =                 args.api_key_id,
                private_key_path =       args.api_key_file,
                signing_scheme =         signing_scheme,
                signing_algorithm =      signing_algorithm,
                hash_algorithm =         intersight.signing.HASH_SHA256,
                signed_headers =         [intersight.signing.HEADER_REQUEST_TARGET,
                                            intersight.signing.HEADER_CREATED,
                                            intersight.signing.HEADER_EXPIRES,
                                            intersight.signing.HEADER_HOST,
                                            intersight.signing.HEADER_DATE,
                                            intersight.signing.HEADER_DIGEST,
                                            'Content-Type',
                                            'User-Agent'
                                            ],
                signature_max_validity = datetime.timedelta(minutes=5)
            )
    )
  else:
    raise Exception('Must configure at least one authentication scheme')

  if args.ignore_tls:
    configuration.verify_ssl = False
  configuration.debug = True
  configuration.discard_unknown_keys = False
  configuration.disabled_client_side_validations = 'pattern'
  configuration.logger_file = 'audit.log'

  # Defining host is optional and default to https://intersight.com
  apiClient = intersight.ApiClient(configuration)
  apiClient.set_default_header('referer', args.url)
  apiClient.set_default_header('x-requested-with', 'XMLHttpRequest')
  apiClient.set_default_header('Content-Type', 'application/json')

  try:
    # Get list of users
    get_users(apiClient)

  except intersight.OpenApiException as e:
      logger.error("Exception when calling API: %s\n" % e)
      traceback.print_exc()

if __name__== "__main__":
    main()

