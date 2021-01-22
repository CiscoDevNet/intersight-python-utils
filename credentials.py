"""Intersight Credential Helper

This script provides a helper function for configuring an intersight API client instance.
It uses argparse to take in the following CLI arguments:

    url:                The intersight root URL for the api endpoint. (The default is https://intersight.com)
    ignore-tls:         Ignores TLS server-side certificate verification
    api-key-legacy:     Use legacy API client (v2) key
    api-key:            API client key id for the HTTP signature scheme
    api-key-file:       Name of file containing secret key for the HTTP signature scheme

"""


import argparse
import os
import datetime

import intersight

# This argument parser instance should be used within scripts where additional CLI arguments are required
Parser = argparse.ArgumentParser(description='Intersight Python SDK credential lookup')


def config_credentials(description=None):
    """config_credentials configures and returns an Intersight api client

    Arguments:
        description {string}: Optional description used within argparse help

    Returns:
        api_client [intersight.api_client.ApiClient]: base intersight api client class
    """
    if description is not None:
        Parser.description = description
    Parser.add_argument('--url', default='https://intersight.com',
                        help='The Intersight root URL for the API endpoint. The default is https://intersight.com')
    Parser.add_argument('--ignore-tls', action='store_true',
                        help='Ignore TLS server-side certificate verification')
    Parser.add_argument('--api-key-legacy', action='store_true',
                        help='Use legacy API client (v2) key')
    Parser.add_argument(
        '--api-key-id',
        default=os.getenv('INTERSIGHT_API_KEY_ID'),
        help='API client key id for the HTTP signature scheme')
    Parser.add_argument(
        '--api-key-file',
        default=os.getenv('INTERSIGHT_API_PRIVATE_KEY', '~/Downloads/SecretKey.txt'),
        help='Name of file containing secret key for the HTTP signature scheme')

    args = Parser.parse_args()

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

    configuration.proxy = os.getenv('https_proxy')
    api_client = intersight.ApiClient(configuration)
    api_client.set_default_header('referer', args.url)
    api_client.set_default_header('x-requested-with', 'XMLHttpRequest')
    api_client.set_default_header('Content-Type', 'application/json')

    return api_client


if __name__ == "__main__":
    config_credentials()
