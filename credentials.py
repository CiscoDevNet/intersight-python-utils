import argparse
import os
import datetime

import intersight


def config_credentials():
    parser = argparse.ArgumentParser(
        description='Intersight Python SDK credential lookup')
    parser.add_argument('--url', default='https://intersight.com',
                        help='The Intersight root URL for the API endpoint. The default is https://intersight.com')
    parser.add_argument('--ignore-tls', action='store_true',
                        help='Ignore TLS server-side certificate verification')
    parser.add_argument('--api-key-legacy', action='store_true',
                        help='Use legacy API client (v2) key')
    parser.add_argument(
        '--api-key-id',
        default=os.getenv('INTERSIGHT_API_KEY_ID'),
        help='API client key id for the HTTP signature scheme')
    parser.add_argument(
        '--api-key-file',
        default=os.getenv('INTERSIGHT_API_PRIVATE_KEY', '~/Downloads/SecretKey.txt'),
        help='Name of file containing secret key for the HTTP signature scheme')

    args = parser.parse_args()

    if args.api_key_id:
        # HTTP signature scheme.
        if args.api_key_legacy:
            signing_scheme = intersight.signing.SCHEME_RSA_SHA256
            signing_algorithm = intersight.signing.ALGORITHM_RSASSA_PKCS1v15
        else:
            signing_scheme = intersight.signing.SCHEME_HS2019
            signing_algorithm = intersight.signing.ALGORITHM_ECDSA_MODE_FIPS_186_3

        configuration = intersight.Configuration(
            host=args.url,
            signing_info=intersight.HttpSigningConfiguration(
                key_id=args.api_key_id,
                private_key_path=args.api_key_file,
                signing_scheme=signing_scheme,
                signing_algorithm=signing_algorithm,
                hash_algorithm=intersight.signing.HASH_SHA256,
                signed_headers=[intersight.signing.HEADER_REQUEST_TARGET,
                                intersight.signing.HEADER_CREATED,
                                intersight.signing.HEADER_EXPIRES,
                                intersight.signing.HEADER_HOST,
                                intersight.signing.HEADER_DATE,
                                intersight.signing.HEADER_DIGEST,
                                'Content-Type',
                                'User-Agent'
                                ],
                signature_max_validity=datetime.timedelta(minutes=5)
            )
        )
    else:
        raise Exception('Must provide API key information to configure at least one authentication scheme')

    if args.ignore_tls:
        configuration.verify_ssl = False

    apiClient = intersight.ApiClient(configuration)
    apiClient.set_default_header('referer', args.url)
    apiClient.set_default_header('x-requested-with', 'XMLHttpRequest')
    apiClient.set_default_header('Content-Type', 'application/json')

    return apiClient


if __name__ == "__main__":
    config_credentials()
