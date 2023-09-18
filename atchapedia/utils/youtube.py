import requests
from django.conf import settings
from time import sleep
import json
import re

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def convert_PT_to_time(time):
    time = time.replace("PT","")
    if(time != None):
        if('S' not in time):
            time = time + '0S'
        if('M' not in time and 'H' not in time):
            time = '0M' + time
        if('M' not in time and 'H' in time):
            time = time.replace("H","H0M")
        if('H' not in time):
            time = '0H' + time
        
        time = "PT"+time
        
        h, m, s = re.findall('PT(\d+)H(\d+)M(\d+)S',time)[0]
        return int(h)*360 + int(m)*60 + int(s)
    else:
        return 0

def get_channel_info(channel_ids):
    # get channel info by channel ids

    n = 50
    new_list = [channel_ids[i:i+n] for i in range(0,len(channel_ids),n)]    
    response_list = []
    for channel_list in new_list:
        channel_list_str = "&id=".join(channel_list)
        url = f"{settings.YOUTUBE_API_URL}/channels?part=snippet%2CcontentDetails%2Cstatistics&id={channel_list_str}&key={settings.YOUTUBE_API_KEY}"
        response = requests.get(url)

        for youtube in response.json()["items"]:
            response_list.append(youtube)    
    return response_list


def get_video_details(video_ids):
    # get video details by video ids
    n = 50
    new_list = [video_ids[i:i+n] for i in range(0,len(video_ids),n)]
    # for i in range(0,len(video_ids),None):
    #     video_ids[i:i+n]
    
    response_list = []
    for video_list in new_list:
        video_list_str = "&id=".join(video_list)
        url = f"{settings.YOUTUBE_API_URL}/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_list_str}&key={settings.YOUTUBE_API_KEY}"
        response = requests.get(url)
        try:
            for youtube in response.json()["items"]:
                response_list.append(youtube)
        except:
            print(response.json())
            
    return response_list
        
    # video_list_str = "&id=".join(video_ids)
    # url = f"{settings.YOUTUBE_API_URL}/videos?part=snippet%2CcontentDetails%2Cstatistics&id={video_list_str}&key={settings.YOUTUBE_API_KEY}"
    # response = requests.get(url)
    # return response.json()

def get_playlist_info(playlist_id):
    # get playlist info by playlist id
    url = f"{settings.YOUTUBE_API_URL}/playlistItems?part=snippet%2CcontentDetails&maxResults=50&&playlistId={playlist_id}&key={settings.YOUTUBE_API_KEY}"
    response = requests.get(url)
    return response.json()


def create_playlist(ACCESS_TOKEN):
#     curl --request POST \
#   'https://youtube.googleapis.com/youtube/v3/playlists?part=snippet%2Cstatus&key=[YOUR_API_KEY]' \
#   --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
#   --header 'Accept: application/json' \
#   --header 'Content-Type: application/json' \
#   --data '{"snippet":{"title":"Sample playlist created via API","description":"This is a sample playlist description.","tags":["sample playlist","API call"],"defaultLanguage":"en"},"status":{"privacyStatus":"private"}}' \
#   --compressed
    # convert above curl to python requests
    headers.Authorization = f"Bearer {ACCESS_TOKEN}"

    url = f"{settings.YOUTUBE_API_URL}/playlists?part=snippet%2Cstatus&key={settings.YOUTUBE_API_KEY}"
    data = {
        "snippet": {
            "title": "[원투차트] 플레이리스트",
            "description": "원투차트에서 찜한 플레이리스트 입니다. https://chart.wantu.io 에서 더 많은 시리즈 콘텐츠를 확인해보세요",
            "tags": [
                "Wantu",
                "Wantu chart",
                "원투",
                "원투 차트"
            ],
            "defaultLanguage": "ko"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

# {
#   "kind": "youtube#playlist",
#   "etag": "34VSyMeWvkh4SFBXe3Mt49O96q8",
#   "id": "PLvf4sBTJ0FqZPoUVR0TDS1YmNKd0Rfy6f",
#   "snippet": {
#     "publishedAt": "2023-08-29T03:33:30Z",
#     "channelId": "UC3sIqj8MMI_c3heXf0L5GIA",
#     "title": "[원투차트] 플레이리스트",
#     "description": "원투차트에서 찜한 플레이리스트 입니다. https://chart.wantu.io 에서 더 많은 시리즈 콘텐츠를 확인해보세요",
#     "thumbnails": {
#       "default": {
#         "url": "https://i.ytimg.com/img/no_thumbnail.jpg",
#         "width": 120,
#         "height": 90
#       },
#       "medium": {
#         "url": "https://i.ytimg.com/img/no_thumbnail.jpg",
#         "width": 320,
#         "height": 180
#       },
#       "high": {
#         "url": "https://i.ytimg.com/img/no_thumbnail.jpg",
#         "width": 480,
#         "height": 360
#       }
#     },
#     "channelTitle": "Yoonseok Choi",
#     "defaultLanguage": "ko",
#     "localized": {
#       "title": "[원투차트] 플레이리스트",
#       "description": "원투차트에서 찜한 플레이리스트 입니다. https://chart.wantu.io 에서 더 많은 시리즈 콘텐츠를 확인해보세요"
#     }
#   },
#   "status": {
#     "privacyStatus": "public"
#   }
# }    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def add_to_playlist(playlistId,videoId, ACCESS_TOKEN):
#     curl --request POST \
#   'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&key=[YOUR_API_KEY]' \
#   --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
#   --header 'Accept: application/json' \
#   --header 'Content-Type: application/json' \
#   --data '{"snippet":{"playlistId":"YOUR_PLAYLIST_ID","position":0,"resourceId":{"kind":"youtube#video","videoId":"M7FIvfx5J10"}}}' \
#   --compressed

    # convert above curl to python requests
    headers.append({"Authorization": f"Bearer {ACCESS_TOKEN}"})
    url = f"{settings.YOUTUBE_API_URL}/playlistItems?part=snippet&key={settings.YOUTUBE_API_KEY}"
    data = {
        "snippet": {
            "playlistId": playlistId,
            "position": 0,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": videoId
            }
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def comment(videoId, text, ACCESS_TOKEN):
# curl --request POST \
#   'https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&key=[YOUR_API_KEY]' \
#   --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
#   --header 'Accept: application/json' \
#   --header 'Content-Type: application/json' \
#   --data '{"snippet":{"videoId":"YOUR_VIDEO_ID","topLevelComment":{"snippet":{"textOriginal":"This is the start of a comment thread."}}}}' \
#   --compressed
    # convert above curl to python requests
    print(ACCESS_TOKEN)
    headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    url = f"{settings.YOUTUBE_API_URL}/commentThreads?part=snippet&key={settings.YOUTUBE_API_KEY}"
    data = {
        "snippet": {
            "videoId": videoId,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": text
                }
            }
        }
    }
                   
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())
    return response.json()

def get_comments(videoId):
    url = f"{settings.YOUTUBE_API_URL}/commentThreads?part=snippet&maxResults=50&order=relevance&videoId={videoId}&key={settings.YOUTUBE_API_KEY}"
    response = requests.get(url)
    return response.json()

def get_highlights(video_ids):
    n = 50
    new_list = [video_ids[i:i+n] for i in range(0,len(video_ids),n)]
    
    response_list = []
    for video_list in new_list:
        video_list_str = "&id=".join(video_list)
        url = f"{settings.LOCAL_YOUTUBE_API_URL}/videos?part=mostReplayed&id={video_list_str}"
        response = requests.get(url)

        for youtube in response.json()["items"]:
            response_list.append(youtube)    
    return response_list