import os
import numpy as np
import pandas as pd
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service_sacc():
    """
    Могу читать и (возможно) писать в таблицы кот. выдан доступ
    для сервисного аккаунта приложения
    sacc-1@privet-yotube-azzrael-code.iam.gserviceaccount.com
    :return:
    """
    creds_json = "key.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


service = get_service_sacc()
# https://docs.google.com/spreadsheets/d/xxx/edit#gid=0
sheet_id = "1CMaM5RILPcNs1sa3Q3DOfx6dgq9c_k3D"
sheet = service.files().copy(fileId=sheet_id,convert=true, body={"title": "specifyName"}).execute()

#sheet = service.spreadsheets()



# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
resp = sheet.values().get(spreadsheetId=sheet_id, range="Orders!A1:AJ9213").execute()

# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet
# resp = sheet.values().batchGet(spreadsheetId=sheet_id, ranges=["Лист1", "Лист2"]).execute()

data = pd.DataFrame(data=resp['values'])

print(data.head())