import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app.utils.youtube import add_playlist_videos
import re

# 사용하려는 API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# 인증정보 파일을 통한 인증
credentials = ServiceAccountCredentials.from_json_keyfile_name('../Wantu-Chart IAM.json', scope)

gc = gspread.authorize(credentials)

# 구글 스프레드시트의 이름
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1-1j55mkrY_Tyi8K2TT9eGJiRA1wcychZIbOC5kOoUoQ/edit#gid=1600710680'

# 스프레드시트 열기
doc = gc.open_by_url(spreadsheet_url)
# a 시트 불러오기
worksheet = doc.get_worksheet(6)
# 모든 데이터 가져오기
data = worksheet.get_all_values()

print(data)

# 특정 셀 데이터 가져오기
data = data[1:]
for item in data:
    if item[0] != '완료':
        playlist = item[5]
        genre = item[6]
        cleaned_text = re.sub("[0-9. ]", "", genre)

        print(playlist, cleaned_text)
        add_playlist_videos(playlist, True)
        worksheet.update_acell('A'+str(data.index(item)+2), '완료')

        #32. 게임


