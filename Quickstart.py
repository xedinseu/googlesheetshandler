import os
import numpy as np
import pandas as pd
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service_sacc():
    """
    Могу читать  в таблицы коорым выдан доступ
    для сервисного аккаунта приложения
    googlesheetshandler@isentropic-disk-332911.iam.gserviceaccount.com
    :return:
    """
    creds_json = "key.json" # файлик с ключами для нашего сервисного аккаунта
    scopes = ['https://www.googleapis.com/auth/spreadsheets'] # разрешения, нужные для обработчика таблиц

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http()) # авторизуем наш сервисный аккаунт
    return build('sheets', 'v4', http=creds_service) # возвращаем коннект к api


def get_service_drive():
    # сервис для drive
    creds_json = "key.json" # файлик с ключами для нашего сервисного аккаунта
    scopes = ['https://www.googleapis.com/auth/drive'] # разрешения, нужные для drive
    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes) # авторизуем наш сервисный аккаунт
    return build('drive', 'v2', credentials=creds_service) # возвращаем коннект к api


# https://docs.google.com/spreadsheets/d/xxx/edit#gid=0
sheet_id = "1CMaM5RILPcNs1sa3Q3DOfx6dgq9c_k3D" # id документа, из которого выгружаем данные

service = get_service_drive() # конектимся к drive фзг
sheet = service.files().copy(fileId=sheet_id,convert=True, body={"title": "specifyName"}).execute() # делаем копию нашего файла, автоматически конвертируя его к стандартному формату
sheet_id = sheet['id'] # извлекаем его id для передачи в обработчик таблиц

service = get_service_sacc() # конектимся к api таблиц
sheet = service.spreadsheets() # создаем объект, работающий с таблицами

# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
resp = sheet.values().get(spreadsheetId=sheet_id, range="Orders!A1:AJ9213").execute() # копируем все данные из листа Orders области A1:AJ921

# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet  батчевые запросы
# resp = sheet.values().batchGet(spreadsheetId=sheet_id, ranges=["Лист1", "Лист2"]).execute()

data = pd.DataFrame(data=resp['values'][1:], columns = resp['values'][0]) # получаем датафрейм из содержимого таблицы

print(data.head())
# А из пандаса данные уже преобразовывать для вывода в sql несложно и понятно