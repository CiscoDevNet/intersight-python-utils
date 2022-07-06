#!/usr/bin/env python
import datetime
from posix import environ
import time
import xlsxwriter
import sys
import os
from dotenv import load_dotenv
import requests
import json
import intersight
from intersight.api import equipment_api
from dateutil import parser

load_dotenv()

def lookup_by_pid(pid):
    lookup = requests.get("https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/" + pid + "?responseencoding=json",headers={'Authorization': 'Bearer ' + CiscoAPIConsoleToken})
    time.sleep(1)
    return json.loads(lookup.text)['EOXRecord']

def find_eos_record(model):
    try:
        for record in eoxdata:
            if record['EOLProductID'] == model:
                return record
    except:
        pass

#setup a configuration object for the Intersight API
configuration = intersight.Configuration(
    signing_info=intersight.HttpSigningConfiguration(
        key_id=os.environ.get('IntersightKeyId'),
        private_key_path=os.environ.get('IntersightSecretKey'),
        signing_scheme=intersight.signing.SCHEME_HS2019,
        signed_headers=[intersight.signing.HEADER_HOST,
                        intersight.signing.HEADER_DATE,
                        intersight.signing.HEADER_DIGEST,
                        intersight.signing.HEADER_REQUEST_TARGET
                        ]
    )
)

#setup a configuration for the EoX API
CiscoEoXAPIKey = os.environ.get('CiscoEoXAPIKey')
CiscoEoXAPISecret = os.environ.get('CiscoEoXAPISecret')
CiscoOauth2Endpoint = "https://cloudsso.cisco.com/as/token.oauth2"
try:
    #get an access token from the oauth2 endpoint
    access_token_response = requests.post(CiscoOauth2Endpoint, data={'grant_type': 'client_credentials'}, verify=True, allow_redirects=False, auth=(CiscoEoXAPIKey, CiscoEoXAPISecret))
    #extract the token from the response
    CiscoAPIConsoleToken = json.loads(access_token_response.text)['access_token']
except:
    print("Failed to get api token from oauth2")

#setup an excel spreadsheet for the output
report_workbook = xlsxwriter.Workbook("Intersight_EoX_Report." + datetime.datetime.now().strftime('%Y-%m-%d.%H%M%S') + ".xlsx", {'remove_timezone': True})
inventory_worksheet = report_workbook.add_worksheet("Inventory")
inventory_worksheet.set_column(0,0,30)
inventory_worksheet.set_column(1,1,17)
inventory_worksheet.set_column(2,2,20)
inventory_worksheet.set_column(3,5,20)
inventory_worksheet.set_column(6,6,10)
inventory_worksheet.set_column(7,13,27)
date_format = report_workbook.add_format({'num_format': 'd mmmm yyyy'})
red_format = report_workbook.add_format({'bold': True, 'font_color': 'red'})
row = 1
column = 0

#SKUs keeps a list of the unique skus that we find
SKUs = []
#eoxdata holds all of the records that we retrieve from the EoX API
eoxdata = []

with intersight.ApiClient(configuration) as api_client:
    api_instance = equipment_api.EquipmentApi(api_client) #get an API instance ready
    select = "Model,Serial,SourceObjectType,RegisteredDevice" #only return the data we need to improve performance
    filter = "Serial ne ''" #only return serialized items
    expand = "RegisteredDevice($select=ConnectionStatus,ConnectionStatusLastChangeTime)" #expand the RegisteredDevice to get connection status
    recordcount = api_instance.get_equipment_device_summary_list(count=True, filter=filter) #check to see how many items we're going to get
    print(str(recordcount.count) + " records found")
    records_per_page = 20 #change this number to control how many results are returned at a time from Intersight
    for i in range(0, recordcount.count, records_per_page):
        query = api_instance.get_equipment_device_summary_list(top=records_per_page, skip=i, select=select, filter=filter, expand=expand, _preload_content=False)
        results = json.loads(query.data)['Results']
        for record in results:
            if record['Model'] not in SKUs: #check to see if this is a new model
                SKUs.append(record['Model']) #add it to the known models if it is
                eoxquery = lookup_by_pid(record['Model'])[0] #request EoX data from the API
                if eoxquery['EOLProductID'] == record['Model']: eoxdata.append(eoxquery) #check to make sure the data is good, and store it
            eoxrecord = find_eos_record(record['Model']) #get the EoX data for the model out of our list
            #write out all of the data into a row of the spreadsheet
            column = 0
            inventory_worksheet.write(row, column, record['Moid'])
            column += 1
            if record['RegisteredDevice']['ConnectionStatus'] == "Connected": #make the cell have red text if it's not currently connected to Intersight
                inventory_worksheet.write(row, column, record['RegisteredDevice']['ConnectionStatus'])
            else:
                inventory_worksheet.write(row, column, record['RegisteredDevice']['ConnectionStatus'], red_format)
            column += 1
            inventory_worksheet.write_datetime(row, column, parser.parse(record['RegisteredDevice']['ConnectionStatusLastChangeTime']), date_format)
            column += 1
            inventory_worksheet.write(row, column, record['Model'])
            print(record['Model'], end =" ")
            column += 1
            inventory_worksheet.write(row, column, record['Serial'])
            print(" " + record['Serial'], end =" ")
            column += 1
            inventory_worksheet.write(row, column, record['SourceObjectType'])
            column += 1
            if eoxrecord: #leave these columns blank if there isn't an eox record
                inventory_worksheet.write(row, column, eoxrecord['ProductBulletinNumber'])
                print(" " + eoxrecord['ProductBulletinNumber'])
                column += 1
                inventory_worksheet.write(row, column, eoxrecord['EndOfSaleDate']['value'])
                column += 1
                inventory_worksheet.write(row, column, eoxrecord['EndOfSWMaintenanceReleases']['value'])
                column += 1
                inventory_worksheet.write(row, column, eoxrecord['EndOfRoutineFailureAnalysisDate']['value'])
                column += 1
                inventory_worksheet.write(row, column, eoxrecord['EndOfSecurityVulSupportDate']['value'])
                column += 1
                inventory_worksheet.write(row, column, eoxrecord['EndOfSvcAttachDate']['value'])
                column += 1
                inventory_worksheet.write(row, column, eoxrecord['EndOfServiceContractRenewal']['value'])
                column += 1
                inventory_worksheet.write(row, column, eoxrecord['LastDateOfSupport']['value'])
            else:
                print(" ...EoX not found.")
            row += 1

#make the data into a table with headers
inventory_worksheet.add_table(0,0,row-1,13,{'columns': [{'header': 'MOID'},
                                                        {'header': 'ConnectionStatus'},
                                                        {'header': 'LastStatusChange'},
                                                        {'header': 'Model'},
                                                        {'header': 'Serial'},
                                                        {'header': 'Type'},
                                                        {'header': 'Bulletin'},
                                                        {'header': 'EndOfSaleDate'},
                                                        {'header': 'EndOfSWMaintenanceDate'},
                                                        {'header': 'EndOfFailureAnalysis'},
                                                        {'header': 'EndOfSecuritySupportDate'},
                                                        {'header': 'EndOfServiceAttach'},
                                                        {'header': 'EndOfServiceContractRenewal'},
                                                        {'header': 'LastDateOfSupport'}]})

#write the workbook
report_workbook.close()
sys.exit(0)