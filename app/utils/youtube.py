import requests
from django.conf import settings
from time import sleep
import json
import re
from googleapiclient.discovery import build #pip install google-api-python-client 필요
from googleapiclient.errors import HttpError
from movies.models import Movie, Episode, DailyView, DailyRank, WeeklyRank, MonthlyRank
import time
from datetime import datetime

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

API_KEY_LIST = ['AIzaSyC9NVqk0XjmU3BP26njxMJoQWmmg0IjlJQ',  
                'AIzaSyDlo1ez9E0Zh81kij8v4Ipx0NWVRrocx0w',
                'AIzaSyDHABt7h3oLJiC64F3QPdBt8DKY7BwDckw',
                'AIzaSyBq0C0uc7rGb_Lw48jOEFjX8R9_mTaOMbA',
                'AIzaSyBySiC-sAvZFKUTRvQqW9LHf5uh5QfwTd4'
                ]

API_INDEX = 0

def make_video_info_request(videoId):
    print("MakeVIDEOINFOREQUEST")
    global API_KEY
    global API_INDEX
    API_KEY = API_KEY_LIST[API_INDEX]  # YouTube Data API 키   
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try :
       print("VideoId:",videoId)

       return youtube.videos().list(
        id=videoId,
        part='snippet,contentDetails,statistics',
        ).execute()
    except HttpError as e:
       if e.resp.status == 404:
          print("Resource not found. Handle 404 error here.")
          pass          
       
       if e.resp.status == 403 and 'quotaExceeded' in e.content:
          print("Quota exceeded. Waiting before retrying...")
          # Wait for some time before retrying (e.g., wait for 1 minute)
          time.sleep(60)
          # Retry the API request
          print("This APIKEY IS EXHAUSTED", API_KEY)
          API_INDEX += 1
          make_video_info_request(videoId)

       else: # Handle other errors
          print(f"Error: {e}")
          pass




# Adding new data

def make_api_request(playlist):
    global API_KEY
    global API_INDEX
    API_KEY = API_KEY_LIST[API_INDEX]  # YouTube Data API 키   
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    try :
        print(playlist)
        max_results = 50
        # Initialize the nextPageToken
        next_page_token = None
        all_playlist_items = []

        # Keep fetching pages until there are no more pages
        while True:
            # Make a request to the playlistItems endpoint
            playlist_items_request = youtube.playlistItems().list(
                playlistId=playlist,
                part='snippet',
                maxResults=max_results,
                pageToken=next_page_token
            )

            # Execute the request and get the response
            playlist_items_response = playlist_items_request.execute()
            # Append items on the current page to the list
            all_playlist_items.extend(playlist_items_response['items'])

            # Check if there are more pages
            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break  # No more pages, exit the loop

        return all_playlist_items
    except HttpError as e:
       if e.resp.status == 404:
          print("Resource not found. Handle 404 error here.")
          pass          
       
       if e.resp.status == 403 and 'quotaExceeded' in e.content:
          print("Quota exceeded. Waiting before retrying...")
          # Wait for some time before retrying (e.g., wait for 1 minute)
          time.sleep(60)
          # Retry the API request
          print("APIKEY IS EXHAUSTED")
          API_INDEX += 1
          make_api_request(playlist)

       else: # Handle other errors
          print(f"Error: {e}")
          pass

def get_video_ids(playlist_response):
    video_ids = []

    for episode in playlist_response:
        video_id = episode['snippet']['resourceId']['videoId']
        video_ids.append(video_id)

    return video_ids

def process_playlist(playlist_response):
    batch_size = 49
    all_video_info = []

    for i in range(0, len(playlist_response), batch_size):
        # Get a batch of video IDs
        batch_video_ids = playlist_response[i:i + batch_size]
        batch_video_info = []
        # Make API request for the current batch
        try:
            batch_video_info = make_video_info_request(batch_video_ids)
        except HttpError as e:
            print(f"Caught a TypeError: {te}")
            print("This APIKEY IS EXHAUSTED", API_KEY)
            API_INDEX += 1
            batch_video_info = make_video_info_request(batch_video_ids)
        # Integrate the results into the overall list
        all_video_info.extend(batch_video_info['items'])
        
    print("RETURN ALL VIDEO INFO")
    return all_video_info

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
    print("GET HIGHLIGHT...")
    response_list = []
    for video_list in new_list:
        video_list_str = "&id=".join(video_list)
        url = f"{settings.LOCAL_YOUTUBE_API_URL}/videos?part=mostReplayed&id={video_list_str}"
        response = requests.get(url)

        for youtube in response.json()["items"]:
            response_list.append(youtube)    
    return response_list


def add_playlist_videos(playlist, highlight=False):
    global API_INDEX
    try:
        playlist_response = make_api_request(playlist)
        print("playlist_response passed")
        # 동영상 수
        # video_count = playlist_response['pageInfo']['totalResults']
        video_count = len(playlist_response)
    except HttpError as e:
        if e.resp.status == 404:
            print("Resource not found. Handle 404 error here.")
            pass          
        
        if e.resp.status == 403 and 'quotaExceeded' in e.content:
            print("Quota exceeded. Waiting before retrying...")
            # Wait for some time before retrying (e.g., wait for 1 minute)
            time.sleep(60)
            # Retry the API request
            print("This APIKEY IS EXHAUSTED", API_KEY)
            API_INDEX += 1
            make_api_request(playlist)

        else: # Handle other errors
            print(f"Error: {e}")
            pass
    except TypeError as te:
        print(f"Caught a TypeError: {te}")
        print("APIKEY IS EXHAUSTED")

        API_INDEX += 1
        make_api_request(playlist)
        # Handle the TypeError here, possibly by providing a default value or logging the issue

    except Exception as e:
        print("ERROR")
        pass
    # 각 동영상의 조회수 가져오기
    total_view_count = 0
    total_comment_count = 0
    total_like_count = 0
    total_dislike_count = 0
    movie = Movie.objects.get(playlist=playlist)


    try:
        video_ids = get_video_ids(playlist_response)
        integrated_video_info = process_playlist(video_ids)
        print("integrated_video_info",integrated_video_info)
        for episode in integrated_video_info:
            video_data = episode['statistics']
            # 조회수
            view_count = int(video_data['viewCount']) if 'viewCount' in video_data else 0
            total_view_count += int(view_count)

            # 댓글 수
            comment_count = int(video_data['commentCount']) if 'commentCount' in video_data else 0
            total_comment_count += int(comment_count)

            # 좋아요 수
            like_count = int(video_data['likeCount']) if 'likeCount' in video_data else 0
            total_like_count += int(like_count)

            # 싫어요 수
            dislike_count = int(video_data['dislikeCount']) if 'dislikeCount' in video_data else 0
            total_dislike_count += int(dislike_count)

            duration = episode['contentDetails']['duration'] if 'duration' in episode['contentDetails'] else 0
            tags = episode['snippet']['tags'] if 'tags' in episode['snippet'] else []

            print(view_count, comment_count, like_count, dislike_count, duration)

            episodeTitle = episode['snippet']['title']
            episodeId = episode['id']
            episodePublishedAt = episode['snippet']['publishedAt']
            episodePublishedAt = datetime.strptime(episodePublishedAt, '%Y-%m-%dT%H:%M:%SZ')
            episodeDescription = episode['snippet']['description']
            episodeTags = tags
            episodeViewCount = view_count
            episodeLikeCount = like_count
            episodeCommentCount = comment_count
            episodeDislikeCount = dislike_count
            episodeDuration = duration

            if highlight:
                try:
                    highlight = get_highlights([episodeId])[0]['mostReplayed']
                    episodeHighlights = {"start": highlight['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeStartMillis'], "end":highlight['heatMarkersDecorations'][0]['timedMarkerDecorationRenderer']['visibleTimeRangeEndMillis']}
                except :
                    episodeHighlights = {"start":0, "end":5000}

            print("Updating new_episode", episodeTitle)
            episode_defaults = {
                'name': episodeTitle,
                'description': episodeDescription,
                'release_date': episodePublishedAt,
                'viewCount': episodeViewCount,
                'likeCount': episodeLikeCount,
                'commentCount': episodeCommentCount,
                'dislikeCount': episodeDislikeCount,
                'duration': episodeDuration,
                'tags': episodeTags,
            }
            if highlight:
                episode_defaults['highlights'] = episodeHighlights


            matching_records = Episode.objects.filter(link=episodeId)
            if matching_records.count() > 1:
                print("Found duplicate records for episode", episodeId)
                # Choose the record you want to keep (for example, the one with the lowest id)
                record_to_keep = matching_records.order_by('id').first()
                # Delete other records
                other_records = matching_records.exclude(pk=record_to_keep.pk)
                other_records.delete()

            new_episode, new_episode_created = Episode.objects.update_or_create(link=episodeId, defaults=episode_defaults)
            print("new_episode_created", new_episode_created)
            print("new_episode", new_episode)
            print("Updating new_episode to movie", new_episode.pk)
            print(new_episode.viewCount,"This should not be 0...")

            movie.episode.through.objects.update_or_create(movie_id=movie.id, episode_id=new_episode.pk)

            # Update DailyView table
            defaults = {'views': episodeViewCount, 'likes': episodeLikeCount, 'comments': episodeCommentCount, 'dislikes': dislike_count }
            print("UPDATED!!!!")

            new_daily_view, new_daily_view_created = DailyView.objects.update_or_create(episode_id=new_episode.pk, date=datetime.now().date(), defaults=defaults)
            print("Updating new_episode to new_daily_view")
        if movie.total_videos != video_count:
          movie.is_new = True
        else:
            movie.is_new = False

        pre_total_videos = movie.total_videos
        pre_total_views = movie.total_views
        pre_total_likes = movie.total_likes
        pre_total_comments = movie.total_comments
        pre_total_dislikes = movie.total_dislikes
        
        movie.total_videos = video_count
        movie.total_views = total_view_count
        movie.total_comments = total_comment_count
        movie.total_likes = total_like_count
        movie.total_dislikes = total_dislike_count

        changed_video_counnt = video_count - pre_total_videos
        changed_view_count = total_view_count - pre_total_views
        changed_like_count = total_like_count - pre_total_likes
        changed_comment_count = total_comment_count - pre_total_comments
        changed_dislike_count = total_dislike_count - pre_total_dislikes


        # Get wantu score by increased view counts only.. 
        movie.wantu_score = changed_view_count + changed_like_count * 10 + changed_comment_count * 5 + changed_dislike_count * -15
        movie.save()

    except IndexError as e:
        print(f"IndexError: {e}. The index is out of range for the list.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    except HttpError as e:
          if e.resp.status == 404:
              print("Resource not found. Handle 404 error here.")
              pass

          if e.resp.status == 403 and 'quotaExceeded' in e.content:
              print("Quota exceeded. Waiting before retrying...")
              # Wait for some time before retrying (e.g., wait for 1 minute)
              time.sleep(60)
              # Retry the API request
              print("This APIKEY IS EXHAUSTED", API_KEY)
              API_INDEX += 1
              make_api_request(playlist)
          else:
              # Handle other errors
              print(f"Error: {e}")

    except TypeError as te:
        print(f"Caught a TypeError: {te}")
        print("This APIKEY IS EXHAUSTED", API_KEY)
        API_INDEX += 1
        make_api_request(playlist)

    except ValueError as outer_ve:
          # Handle the error in the outer try block
          print(f"Caught an outer error: {outer_ve}")



def update_daily_rank():

    # Get wantu score of each movie
    movies = Movie.objects.all()
    
    for movie in movies:
        # Get wantu score of each movie
        movie.wantu_score

        # GET list of yesterday's daily ranks
        yesterday = datetime.now().date() - datetime.timedelta(days=1)
        yesterday_ranks = DailyRank.objects.filter(date=yesterday, genre='all')

        # sort movies by wantu score
        sorted_movies = Movie.objects.order_by('-wantu_score')
        rank_updates = []
        for index, movie in enumerate(sorted_movies):
            rank_fluctuation = index - yesterday_ranks.rank, 
            rank_updates.append(DailyRank(movie=movie, rank=index+1))

            # { rank:1, rankFluc: 2, movie_id, wantu_score}
            # 

        # Now calculate fluctuation of each movie
        # Get every movie's last day's rank and current rank and calculate fluctuation
        # Get last day's rank



        
        

        # Sort movies by each genre and order by wantu score
        # Get all genres
        genres = movie.genre.all()
        for genre in genres:
            sorted_movies = sorted_movies.filter(genre=genre).order_by('-wantu_score')

        