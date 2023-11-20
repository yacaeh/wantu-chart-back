# import schedule
import time
from datetime import datetime
from googleapiclient.discovery import build #pip install google-api-python-client 필요
import requests

API_KEY = 'AIzaSyDlo1ez9E0Zh81kij8v4Ipx0NWVRrocx0w'  # YouTube Data API 키
youtube = build('youtube', 'AIzaSyBq0C0uc7rGb_Lw48jOEFjX8R9_mTaOMbAv3', developerKey=API_KEY)

# 현재 날짜 및 시간
now = datetime.now()

# 현재 날짜를 년, 월, 일로 분리
year = now.year
month = now.month
day = now.day

print(f"오늘의 날짜: {year}년 {month}월 {day}일")

def my_daily_job():
    now = datetime.now()

    # 현재 날짜를 년, 월, 일로 분리
    year = now.year
    month = now.month
    day = now.day
    print(f"오늘의 날짜: {year}년 {month}월 {day}일")


    PLAYLIST_ID = 'PL98dl1M6shCEuKZbdPquTNTQzG_IQhGz6'  # 조회하고 싶은 플레이리스트 ID

    # 플레이리스트의 동영상 목록 요청
    playlist_response = youtube.playlistItems().list(
        part='snippet',
        playlistId=PLAYLIST_ID
    ).execute()

    # 동영상 수
    video_count = len(playlist_response['items'])
    print(f"플레이리스트 동영상 수: {video_count}")

    # 각 동영상의 조회수 가져오기
    total_view_count = 0
    total_comment_count = 0
    total_like_count = 0
    total_dislike_count = 0

    for video in playlist_response['items']:
        video_id = video['snippet']['resourceId']['videoId']
        print(f"동영상 id: {video_id}")
        video_info = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}')
        video_data = video_info.json()['items'][0]['statistics']

        # 조회수
        view_count = int(video_data['viewCount']) if 'viewCount' in video_data else 0
        print(f"동영상 조회수: {view_count}")
        total_view_count += int(view_count)

        # 댓글 수
        comment_count = int(video_data['commentCount']) if 'commentCount' in video_data else 0
        print(f"동영상 댓글 수: {comment_count}")
        total_comment_count += int(comment_count)

        # 좋아요 수
        like_count = int(video_data['likeCount']) if 'likeCount' in video_data else 0
        print(f"동영상 좋아요 수: {like_count}")
        total_like_count += int(like_count)

        # 싫어요 수
        dislike_count = int(video_data['dislikeCount']) if 'dislikeCount' in video_data else 0
        print(f"동영상 싫어요 수: {dislike_count}")
        total_dislike_count += int(dislike_count)

    print(f"플레이리스트 총 조회수: {total_view_count}")
    print(f"플레이리스트 총 댓글 수: {total_comment_count}")
    print(f"플레이리스트 총 좋아요 수: {total_like_count}")
    print(f"플레이리스트 총 싫어요 수: {total_dislike_count}")

    # 각 데이터를 log 파일로 저장하거나, DB로 담는 로직 필요

# 스케줄링 (예시: 매일 밤 11시)
# schedule.every().day.at("23:00").do(my_daily_job)

while True:
    # schedule.run_pending()
    time.sleep(60)  # 60초마다 스케줄 확인