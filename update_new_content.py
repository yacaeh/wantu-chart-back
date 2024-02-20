import requests
import json
from datetime import datetime, timedelta, timezone

webhook_url = "https://hooks.slack.com/services/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"

def fetch_all_videos(base_url, start_period):
    all_videos = []  # 모든 비디오 정보를 저장할 리스트

    # indexTarget을 1부터 28까지 순회합니다.
    for index_target in range(1, 29):
        # 초기 cursor 값을 설정합니다.
        next_cursor = ""
        while True:
            # API URL을 구성합니다. period와 cursor, indexTarget 값을 업데이트합니다.
            url = f"{base_url}&period={start_period}&cursor={next_cursor}&size=20&chartTypeId=20&periodTypeId=3&indexDimensionId=20&indexTypeId=4&indexTarget={index_target}&indexCountryCode=KR"
            
            response = requests.get(url)
            data = response.json()

            videos = data.get('list', [])
            all_videos.extend(videos)  # 현재 페이지의 비디오를 전체 리스트에 추가

            # 다음 페이지가 있는지 확인하고, 있다면 cursor를 업데이트합니다.
            if data.get('hasNext'):
                next_cursor = data.get('cursor')
            else:
                break  # 다음 페이지가 없으면 반복을 종료합니다.

    return all_videos

# 기본 URL과 시작 period를 설정합니다.
base_url = "https://api.playboard.co/v1/chart/video?locale=ko&countryCode=KR"
start_period = 1707696000  # 예시 period 값

# 함수를 호출하여 모든 비디오 정보를 가져옵니다.
videos = fetch_all_videos(base_url, start_period)

# https://api.playboard.co/v1/chart/video?locale=ko&countryCode=KR&period=1708128000&size=20&chartTypeId=20&periodTypeId=2&indexDimensionId=20&indexTypeId=4&indexTarget=24&indexCountryCode=KR
# https://api.playboard.co/v1/chart/video?locale=ko&countryCode=KR&period=1708214400&cursor=04123b3688bf1b6d8d736e27557fcc96:bb4923a66aee9f4ee60566ff185ef86699e787d57a5d25a58036270c1dcec0f30f866368fe45584087fcc7a6bb0bc3dae96b1c23733c394ae707319fa0e14ee8&size=20&chartTypeId=20&periodTypeId=2&indexDimensionId=20&indexTypeId=4&indexTarget=17&indexCountryCode=KR
# 모든 비디오 정보 출력
# for i, video in enumerate(videos, start=1):
#     title = video['video']['title']
#     play_count = video['video']['playCount']
#     channel_name = video['channel']['name']
    # print(f"{i}. 제목: {title}, 재생 수: {play_count},채널 이름: {channel_name}")

# "ep."가 포함된 제목의 비디오만 필터링
ep_videos = [video for video in videos if 'ep.' in video['video']['title'].lower()]
# 메시지 내용 구성
# "ep."가 포함된 제목의 비디오 목록을 메시지로 구성
message = "\n".join([f"{i}. 채널: {video['channel']['channelId']} 채널명: {video['channel']['name']} 제목: {video['video']['title']} ID: {video['video']['videoId']}"  for i, video in enumerate(ep_videos, start=1)])
data = {"text": message}

# Slack API를 통해 메시지 전송
response = requests.post(webhook_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

# 응답 출력 (확인용)
print(response.text)