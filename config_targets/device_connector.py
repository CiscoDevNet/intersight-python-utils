#!/usr/bin/env python
"""Intersight Device Connector API access classes."""
import re
from xml.etree import ElementTree
from time import sleep
import requests


def requests_op(operation, uri, header, ro_json, body):
    """perform operation and retry on 5XX status errors"""
    for _ in range(10):
        if operation == 'GET':
            resp = requests.get(uri, verify=False, headers=header)
        elif operation == 'PUT':
            resp = requests.put(uri, verify=False, headers=header, json=body)
        else:
            ro_json['ApiError'] = "unsupported operation %s" % (operation)
            break

        if re.match(r'2..', str(resp.status_code)):
            ro_json.pop('ApiError', None)
            if operation == 'GET':
                if isinstance(resp.json(), list):
                    ro_json = resp.json()[0]
                else:
                    ro_json['ApiError'] = "%s %s %s" % (operation, uri, resp.status_code)
            break
        ro_json['ApiError'] = "%s %s %s" % (operation, uri, resp.status_code)
        if re.match(r'5..', str(resp.status_code)):
            sleep(1)
            continue
        break
    return ro_json


class DeviceConnector():
    """Intersight Device Connector API superclass.
    Managed endpoint access information (hostname, username) and configuration data should be provided in the device dictionary parameter.
    """

    def __init__(self, device):
        self.logged_in = False
        self.auth_header = ''
        self.device = device
        if self.device['device_type'] == 'ucspe':
            self.connector_uri = "http://%s/connector" % self.device['hostname']
        else:
            self.connector_uri = "https://%s/connector" % self.device['hostname']
        self.systems_uri = "%s/Systems" % self.connector_uri

    def get_status(self):
        """Check current connection status."""
        ro_json = dict(AdminState=False)
        # get admin, connection, and claim state
        ro_json = requests_op(operation='GET', uri=self.systems_uri, header=self.auth_header, ro_json=ro_json, body={})
        return ro_json

    def configure_connector(self):
        """Check current Admin state and enable the Device Connector if not currently enabled."""
        ro_json = dict(AdminState=False)
        for _ in range(4):
            ro_json = self.get_status()
            if ro_json['AdminState']:
                break
            # enable the device connector
            ro_json = requests_op(operation='PUT', uri=self.systems_uri, header=self.auth_header, ro_json=ro_json, body={'AdminState': True})
            if ro_json.get('ApiError'):
                break
        return ro_json

    def configure_access_mode(self, ro_json):
        """Configure the Device Connector access mode (ReadOnlyMode True/False)."""
        for _ in range(4):
            # device read_only setting is a bool (True/False)
            ro_json = requests_op(operation='PUT', uri=self.systems_uri, header=self.auth_header, ro_json=ro_json, body={'ReadOnlyMode': self.device['read_only']})
            if ro_json.get('ApiError'):
                break
            # confirm setting has been applied
            ro_json = self.get_status()
            if ro_json['ReadOnlyMode'] == self.device['read_only']:
                break
        return ro_json

    def configure_proxy(self, ro_json, result):
        """Configure the Device Connector proxy if proxy settings (hostname, port) were provided)."""
        # put proxy settings.  If no settings were provided the system settings are not changed
        if self.device.get('proxy_host') and self.device.get('proxy_port'):
            # setup defaults for proxy settings
            if not self.device.get('proxy_password'):
                self.device['proxy_password'] = ''
            if not self.device.get('proxy_username'):
                self.device['proxy_username'] = ''
            proxy_payload = {
                'ProxyHost': self.device['proxy_host'],
                'ProxyPassword': self.device['proxy_password'],
                'ProxyPort': int(self.device['proxy_port']),
                'ProxyType': 'Manual',
                'ProxyUsername': self.device['proxy_username'],
            }
            proxy_uri = "%s/HttpProxies" % self.connector_uri
            for _ in range(4):
                # check current setting
                ro_json = requests_op(operation='GET', uri=proxy_uri, header=self.auth_header, ro_json=ro_json, body={})
                if ro_json.get('ApiError'):
                    break
                if ro_json['ProxyHost'] == self.device['proxy_host'] and ro_json['ProxyPort'] == int(self.device['proxy_port']) and ro_json['ProxyType'] == 'Manual':
                    break
                result['msg'] += "  Setting proxy: %s %s" % (self.device['proxy_host'], self.device['proxy_port'])
                ro_json = requests_op(operation='PUT', uri=proxy_uri, header=self.auth_header, ro_json=ro_json, body=proxy_payload)
                if ro_json.get('ApiError'):
                    break
                result['changed'] = True
            else:
                # finished without matching expected
                ro_json['ApiError'] = 'failed to configure proxy'
            if not ro_json.get('ApiError'):
                # get updated status
                ro_json = self.get_status()
        return ro_json

    def get_claim_info(self, ro_json):
        """Get the Device ID and Claim Code from the Device Connector."""
        claim_resp = {}
        device_id = ''
        claim_code = ''
        # get device id and claim code
        id_uri = "%s/DeviceIdentifiers" % self.connector_uri
        ro_json = requests_op(operation='GET', uri=id_uri, header=self.auth_header, ro_json=ro_json, body={})
        if not ro_json.get('ApiError'):
            device_id = ro_json['Id']

            claim_uri = "%s/SecurityTokens" % self.connector_uri
            ro_json = requests_op(operation='GET', uri=claim_uri, header=self.auth_header, ro_json=ro_json, body={})
            if not ro_json.get('ApiError'):
                claim_code = ro_json['Token']
            else:
                claim_resp['ApiError'] = ro_json['ApiError']
        else:
            claim_resp['ApiError'] = ro_json['ApiError']
        return(claim_resp, device_id, claim_code)


class HxDeviceConnector(DeviceConnector):
    """HyperFlex (HX) Device Connector subclass.
    HX REST API session cookie is used to authenticate Device Connector API access.
    """

    def __init__(self, device):
        super(HxDeviceConnector, self).__init__(device)
        # create HX REST API session
        # --------------------------------
        self.hx_rest_uri = "https://%s/aaa/v1/auth?grant_type=password" % self.device['hostname']
        hx_rest_header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        hx_rest_body = {
            'username': self.device['username'],
            'password': self.device['password'],
            'client_id': 'HxGuiClient',
            'client_secret': 'Sunnyvale',
            'redirect_uri': 'http://localhost:8080/aaa/redirect'
        }
        resp = requests.post(self.hx_rest_uri, verify=False, headers=hx_rest_header, json=hx_rest_body)
        if re.match(r'2..', str(resp.status_code)):
            ro_json = resp.json()
            hx_cookie_str = "test; tokenType=Basic; locale=en; refreshToken=%s; token=%s" % (ro_json['refresh_token'], ro_json['access_token'])
            self.auth_header = {'Cookie': hx_cookie_str}
            self.logged_in = True

    def logout(self):
        """Logout of HX REST API session if currently logged in."""
        if self.logged_in:
            # logout TBD
            self.logged_in = False


class UcsDeviceConnector(DeviceConnector):
    """UCS Manager (UCSM) and Integrated Management Controller (IMC) Device Connector subclass.
    UCS XML API session cookie is used to authenticate Device Connector API access.
    """

    def __init__(self, device):
        super(UcsDeviceConnector, self).__init__(device)
        # XML API login and create session cookie
        # --------------------------------
        self.xml_uri = "https://%s/nuova" % self.device['hostname']
        xml_body = "<aaaLogin inName=\"%s\" inPassword=\"%s\" />" % (self.device['username'], self.device['password'])
        resp = requests.post(self.xml_uri, verify=False, data=xml_body)
        if re.match(r'2..', str(resp.status_code)):
            xml_tree = ElementTree.fromstring(resp.content)
            if not xml_tree.attrib.get('outCookie'):
                return
            self.xml_cookie = xml_tree.attrib['outCookie']
            self.auth_header = {'ucsmcookie': "ucsm-cookie=%s" % self.xml_cookie}
            self.logged_in = True

    def logout(self):
        """Logout of UCS API session if currently logged in."""
        if self.logged_in:
            # XML API logout
            # --------------------------------
            xml_body = "<aaaLogout inCookie=\"%s\" />" % self.xml_cookie
            requests.post(self.xml_uri, verify=False, data=xml_body)
            self.logged_in = False
