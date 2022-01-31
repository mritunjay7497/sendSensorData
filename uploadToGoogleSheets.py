from __future__ import print_function
from multiprocessing.connection import Client

import os.path
from pickle import GLOBAL
from pprint import pprint
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

sheetId = {}

with open("/home/plusx/sendSensorData/sensitiveInfo.json", "r") as sensitiveInfo:
    sheetId['spreadheetId'] = json.load(sensitiveInfo)

SPREADSHEET_ID = sheetId['spreadheetId']['SPREADHSEET_ID']
RANGE_NAME = 'Sheet1'


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/plusx/sendSensorData/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()

        value_input_option = 'USER_ENTERED'

        sensorJson = {}
        with open("sensors.json", "r") as sj:
            sensorJson = json.load(sj)

        currentReading = []

        for sensor in sensorJson.keys():
            currentReading.append([sensor, sensorJson[sensor]])

        request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                         range=RANGE_NAME, valueInputOption=value_input_option, body={"values": currentReading})

        response = request.execute()

        pprint(response)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
    os.system("rm sensors.json")
