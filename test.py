from googleapiclient.discovery import build #pip install google-api-python-client 필요
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def update_googlesheet():
    # 사용하려는 API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # 인증정보 파일을 통한 인증
    credentials = ServiceAccountCredentials.from_json_keyfile_name('IAM.json', scope)

    gc = gspread.authorize(credentials)

    # 구글 스프레드시트의 이름
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1yCDlxxNuHkmZTKkvC5Jh3KLlnS-V17mXDIvs4iuLCZ8'

    # 스프레드시트 열기
    doc = gc.open_by_url(spreadsheet_url)
    # a 시트 불러오기
    all_data = []
    for i, worksheet in enumerate(doc.worksheets()):
        data = worksheet.get_all_values()  # 2D list
        all_data.append({'bricksData': data})

    with open('data.json', 'w') as f:
        json.dump(all_data, f)

update_googlesheet()