'''
Lambda handler to write Intersight Alarm records to Timestream
'''
from datetime import datetime
import os
import json
import logging
import hashlib
import hmac
import base64
from urllib.parse import urlparse

import boto3
from botocore.config import Config

DATABASE_NAME = "intersightTME"
TABLE_NAME = "alarmsTME"

FORMAT = '%(asctime)-15s [%(levelname)s] [%(filename)s:%(lineno)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('openapi')


def prepare_record(timestamp, dimensions, measure_name, measure_value):
    record = {
        'Time': str(timestamp),
        'Dimensions': dimensions,
        'MeasureName': measure_name,
        'MeasureValue': measure_value,
        'MeasureValueType': 'VARCHAR'
    }
    return record


def write_records(write_client, records):
    try:
        result = write_client.write_records(DatabaseName=DATABASE_NAME,
                                            TableName=TABLE_NAME,
                                            Records=records,
                                            CommonAttributes={})
        status = result['ResponseMetadata']['HTTPStatusCode']
        print("Processed %d records. WriteRecords Status: %s" %
              (len(records), status))
    except Exception as err:
        print("Error:", err)


def get_sha256_digest(data):
    """
    Generates a SHA256 digest from a String.
    :param data: data string set by user
    :return: instance of digest object
    """

    digest = hashlib.sha256()
    digest.update(data.encode())

    return digest


def prepare_str_to_sign(req_tgt, hdrs):
    """
    Concatenates Intersight headers in preparation to be signed
    :param req_tgt : http method plus endpoint
    :param hdrs: dict with header keys
    :return: concatenated header authorization string
    """
    sign_str = ""
    sign_str = sign_str + "(request-target): " + req_tgt + "\n"

    length = len(hdrs.items())

    i = 0
    for key, value in hdrs.items():
        sign_str = sign_str + key.lower() + ": " + value
        if i < length - 1:
            sign_str = sign_str + "\n"
        i += 1

    return sign_str


def get_auth_header(hdrs, signed_msg, key_id):
    """
    Assmeble an Intersight formatted authorization header
    :param hdrs : object with header keys
    :param signed_msg: base64 encoded sha256 hashed body
    :return: concatenated authorization header
    """

    auth_str = "Signature"

    auth_str = auth_str + " " + "keyId=\"" + key_id + "\", " + "algorithm=\"" + 'hmac-sha256' + "\","

    auth_str = auth_str + " headers=\"(request-target)"

    for key, dummy in hdrs.items():
        auth_str = auth_str + " " + key.lower()
    auth_str = auth_str + "\""

    auth_str = auth_str + "," + " signature=\"" + signed_msg.decode('ascii') + "\""

    return auth_str


def verify_auth_header(event):
    if event.get('headers'):
        actual_auth = event['headers']['Authorization']
        print('>>   actual_auth:', actual_auth)
    else:
        raise Exception("No auth header to verify")

    # Generate the expected authorization header
    host_uri = os.getenv('INTERSIGHT_WEBHOOK_URI')
    target_host = urlparse(host_uri).netloc
    target_path = urlparse(host_uri).path
    request_target = 'post' + " " + target_path

    body_digest = get_sha256_digest(event['body'])
    b64_body_digest = base64.b64encode(body_digest.digest())
    auth_header = {
        'Host': target_host,
        'Date': event['headers']['Date'],
        'Digest': "SHA-256=" + b64_body_digest.decode('ascii'),
        'Content-Type': 'application/json',
        'Content-Length': str(len(event['body']))
    }
    if auth_header['Digest'] != event['headers']['Digest']:
        raise Exception("Unexpected body digest")

    string_to_sign = prepare_str_to_sign(request_target, auth_header)
    print('>> string to sign:', string_to_sign)
    webhook_secret = os.getenv('INTERSIGHT_WEBHOOK_SECRET')
    sign = hmac.new(webhook_secret.encode(), msg=string_to_sign.encode(), digestmod=hashlib.sha256).digest()
    b64_signature = base64.b64encode(sign)
    key_id = os.getenv('INTERSIGHT_WEBHOOK_KEY_ID')
    expected_auth = get_auth_header(auth_header, b64_signature, key_id)
    print('>> expected auth:', expected_auth)

    if expected_auth != actual_auth:
        raise Exception("Authorization failed")


def lambda_handler(event, context):
    print('>> event:', event)
    print('>> context:', context)
    verify_auth_header(event)

    # Code below is specific to AWS Timestream and not required for processing Intersight webhooks
    session = boto3.Session()
    write_client = session.client('timestream-write', config=Config(
        read_timeout=20, max_pool_connections=5000, retries={'max_attempts': 10}))
    records = []

    # Code below is specific to Intersight Alarm resources.  Other webhook resource types would have different attributes.
    alarm_event = json.loads(event['body'])['Event']
    print('>> alarm:', alarm_event['LastTransitionTime'], alarm_event['AffectedMoDisplayName'], alarm_event['Code'], alarm_event['Moid'])
    # timestamp = int(datetime.fromisoformat(alarm_event['LastTransitionTime']).timestamp() * 1000)
    timestamp = int(datetime.strptime(alarm_event['LastTransitionTime'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp() * 1000)
    print('>> timestamp:', timestamp)
    dimensions = [
        {'Name': 'affected_mo', 'Value': alarm_event['AffectedMoDisplayName']},
        {'Name': 'device', 'Value': alarm_event['Moid']}
    ]
    records.append(prepare_record(timestamp, dimensions, 'alarm_code', alarm_event['Code']))

    write_records(write_client, records)

    resp = {
        "statusCode": 200,
        "isBase64Encoded": False
    }
    print(resp)
    return resp


if __name__ == '__main__':
    test_event = []
    test_context = []
    lambda_handler(test_event, test_context)
