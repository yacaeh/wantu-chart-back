# Import everything
from dotenv import load_dotenv
import random
import os
from openai import OpenAI
from gtts import gTTS
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
from moviepy.video.fx import resize
load_dotenv()
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup
import re
import requests
import json
from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, ImageClip, TextClip, CompositeVideoClip,ColorClip
from PIL import Image
from io import BytesIO
import sys
import urllib.request
from textwrap import wrap

# Ask for video info
# title = input("\nEnter the name of the video >  ")
# option = input('Do you want AI to generate content? (yes/no) >  ')
title = "24년 2월 첫째주 유튜브 예능 랭킹"
option = 'yes'
# YouTube Data API 키와 플레이리스트 ID 설정
API_KEY = 'AIzaSyDlo1ez9E0Zh81kij8v4Ipx0NWVRrocx0w'
PLAYLIST_ID = 'PLmtapKaZsgZt3g_uAPJbsMWdkVsznn_2R'
API_URL = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={PLAYLIST_ID}&maxResults=10&key={API_KEY}'
# API 요청하여 데이터 가져오기
response = requests.get(API_URL)
playlist_items = response.json()
# 특수 문자와 이모지를 제거하는 함수
def remove_special_chars_and_emojis(text):
    # 이모지 제거
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    # 특수 문자 제거
    text = re.sub(r'[^\w\s\uAC00-\uD7A3]', '', text)    
    return text

# 썸네일 다운로드 및 저장 함수
def download_and_save_thumbnail(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(save_path)

def extract_and_save_clip(video_path, start_time, end_time, output_path):
    """
    비디오에서 특정 구간을 추출하여 저장하는 함수
    :param video_path: 원본 비디오 파일 경로
    :param start_time: 추출 시작 시간 (초)
    :param end_time: 추출 종료 시간 (초)
    :param output_path: 저장할 파일 경로
    """
    # 비디오 파일 로드
    clip = VideoFileClip(video_path)
    # 특정 구간 추출
    subclip = clip.subclip(start_time, end_time)
    # 추출된 구간 저장
    subclip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# 비디오 다운로드 함수
def download_video(video_id, filename):
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    # 현재 작업 디렉토리에 지정된 파일 이름으로 비디오 저장
    stream.download(filename=filename)

save_path = 'youtube_rank_videos'
if not os.path.exists(save_path):
    os.makedirs(save_path)

def get_video_details(video_id, api_key):
    video_details_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet&key={api_key}"
    response = requests.get(video_details_url)
    video_details = response.json()
    return video_details

# 비디오 정보를 JSON 객체로 변환
videos_info = []
video_info_gpt = []

def get_youtube_data(playlist_items):

    global videos_info
    global video_info_gpt
    # 플레이리스트의 각 비디오에 대한 정보를 반복하여 가져옴
    for index, item in enumerate(playlist_items.get('items', [])):
        video_id = item['snippet']['resourceId']['videoId']
        video_title = item['snippet']['title']
        video_thumbnail = item['snippet']['thumbnails']['high']['url']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video_description = item['snippet']['description']
        channel_title = item['snippet']['channelTitle']  # 채널 이름 추가
        channel_thumbnail = item['snippet']['thumbnails']['default']['url']

        # 썸네일 저장 경로 설정 (PNG 형식으로 저장)
        thumbnail_path = f'{save_path}/{video_id}.png'
        # 썸네일 다운로드 및 저장
        download_and_save_thumbnail(video_thumbnail, thumbnail_path)

        output_path = save_path+'/'+video_id+'_extracted.mp4'
        videos_info.append({
            'title': video_title,
            'url': video_url,
            'description': video_description,
            'thumbnail': thumbnail_path,  # 저장된 썸네일 경로로 업데이트
            'channel': channel_title,
            'video_path': output_path,
            'channel_thumbnail': channel_thumbnail  # JSON 객체에 채널 썸네일 추가
        })

        video_info_gpt.append({
            'title': (video_title),
            'description': (video_description),
            # 'channel': (channel_title),
        })

        # 비디오 다운로드 및 처리 코드는 그대로 유지
        # download_video(video_id, video_id+'.mp4')
        video_path = video_id+'.mp4'
        output_path = save_path+'/'+video_id+'_extracted.mp4'
        # 예시 사용법
        start_time = 10  # 시작 시간 (10초)
        end_time = 15  # 종료 시간 (15초)

        # 함수 호출
        # extract_and_save_clip(video_path, start_time, end_time, output_path)
        # 원본 비디오 파일 삭제
        # os.remove(video_path)

    # JSON 객체 출력
    video_info = json.dumps(videos_info, indent=4, ensure_ascii=False)
    with open('videos_info.json', 'w', encoding='utf-8') as f:
        json.dump(videos_info, f, ensure_ascii=False, indent=4)


    video_info_gpt = json.dumps(video_info_gpt, indent=4, ensure_ascii=False)
    video_info_gpt = remove_special_chars_and_emojis(video_info_gpt)


def get_gpt_response(video_info_gpt):
    print(video_info_gpt)
    # Generate content using OpenAI API
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ["OPENAI_API"]
    )

    sample_content='''오프닝:
"2024년 2월 첫째주 가장 인기 있는 유튜브 콘텐츠"

10위: 새해 인사는 핑계고 ㅣ EP35
"이번 주 10위는 '새해 인사는 핑계고'로, 유재석, 이서진, 양세찬이 새해맞이 떡국 먹방과 솔직담백한 덕담을 나누는 내용이에요. 

9위: 미공개 시즌3 확정하고 먹는 고기가 제일 맛도리 출연 | 행복한 몬스터즈 | 최강야구 비하인드 cam 82
"9위는 '행복한 몬스터즈'의 회식 현장이에요. 

8위: I Spent 7 Days In Solitary Confinement
"8위, MrBeast의 도전기 'I Spent 7 Days In Solitary Confinement'이에요. 

7위: [SUB]전지적 할부지 시점 ep.166 - 모든 게 신기해오! 드디어 밖으로 나온 아루후의 놀이터 나들이 | Panda World
"아이바오 판다 가족의 새로운 모습을 볼 수 있는 '전지적 할부지 시점'이 7위네요. 

6위: 필리핀 숨겨진 섬에서 2023년 마무리 | 필리핀끝
"6위는 '필리핀 숨겨진 섬에서 2023년 마무리'. 

5위: 캠지기 민경훈과 함께하는 한파 속 겨울 캠핑
"민경훈의 겨울 캠핑이 5위를 차지했어요. 

4위: 광안리 M 드론라이트쇼 | 1월 1일 2024 카운트다운 공연 라이브
"2024년 첫 날, 화려한 '광안리 M 드론라이트쇼'로 4위에 올랐네요. 

3위: 떨어지는 비에도 꽃은 피어나니까, 화사 잔잔하지만 가슴을 울리는 축하무대 | LMM | SBS연기대상
"3위는 가수 화사의 감성적인 무대 'LMM'. 

2위: MBC연예대상 기안이 해냈다! 박빙의 대상부터 신인상까지 4시간 연예대상 20분만에 몰아보기ㅣ기안84
"MBC 연예대상의 모든 것을 20분 안에 담은 '기안84'의 영상이 2위를 했어요. 

1위: 2023 기안어워즈
"마지막으로 1위는 '2023 기안어워즈'. 

아웃트로:
"여러분과 함께 본 이번주 톱 10 유튜브 쇼츠였습니다. "'''
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "너는 인공지능을 이용한 유튜브 콘텐츠 순위를 만드는 유튜브 스크립트 메이커야. 제목은 원투차트 선정 00년 00월 00주 유튜브 콘텐츠 순위.  유튜브순위를 10위부터 1위까지 추출하여 각각의 유튜브 제목에 대한 설명을 붙여줘야해. 유튜브 영상링크와 제목이 제공될거야. 총길이 30~60초 이내의 분량으로 만들어야해. 각각 영상의 title, description 데이터를 이용해서 각각 5초이내로 해줘. 순위 정보는 API가 아닌 직접 텍스트로 제공될거야"},
            {"role": "user", "content": f"이번주 유튜브 영상 1위부터 10위 까지의 비디오는 {video_info_gpt} 야. 인트로로 간단한소개와 각각의 비디오의 순위와 짧은 클립을 만들어. 그리고 마지막아웃트로로 마무리해. 실제 내용에 들어갈 답변만 포함해줘. 그리고 각각의 순위의 설명은 50자 이내로. 그리고 순위 시작전 항상 0위, 그리고 설명을 시작해줘 다음 포맷과 똑같이 만들어 {sample_content}"},
            {"role": "assistant", "content": sample_content},  # 이전 대답을 포함
        ],
        model="gpt-4-1106-preview",
    )
    # print(response.choices[0].text)
    print(response)
    content = response.choices[0].message.content

    # content_str = json.dumps(content, ensure_ascii=False, indent=4)

    with open('generated/gpt_script.txt', 'w', encoding='utf-8') as file:
        file.write(content)
    print(content)

    # yes_no = input('\nIs this fine? (yes/no) >  ')
    # if yes_no == 'yes':
    #     content = response.choices[0].message.content
    #     with open('generated/script.txt', 'w', encoding='utf-8') as file:
    #         file.write(content)
    # else:
    #     content = input('\nEnter >  ')
# else:
#     content = input('\nEnter the content of the video >  ')

# Create the directory
if os.path.exists('generated') == False:
    os.mkdir('generated')

def generate_tts():
    # Create the script file
    # 텍스트를 줄 단위로 분리
    loaded_script = open('generated/gpt_script.txt', 'r', encoding='utf-8')
    content = loaded_script.read()
    lines = content.strip().split('\n')

    # 결과를 저장할 배열
    titles = []
    descriptions = []
    # 'temp' 디렉토리가 존재하는지 확인하고, 없으면 생성
    if not os.path.exists('temp'):
        os.makedirs('temp')
    CHUNK_SIZE = 1024

    # 각 줄을 순회하며 처리
    for line in lines:
        if ':' in line and not line.startswith('"'):  # ':'를 포함하고 따옴표로 시작하지 않는 줄
            titles.append(line)
        elif line.startswith('"') and line.endswith('"'):  # 따옴표로 둘러싸인 줄
            descriptions.append(line[1:-1])  # 따옴표 제거

    print("Titles:", titles)
    print("Descriptions:", descriptions)

    # Generate speech for the video
    # gTTS를 사용하여 한국어로 음성 생성
    # Generate each descriptions
    custom_voice = "I7QkOe1ePfqu4VLOD4BS" # I7QkOe1ePfqu4VLOD4BS zEt5ObgwibbeIz86fOyJ
    for i, description in enumerate(descriptions):

        headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ["ELEVENLABS_API"]
        }
        
        data = {
            "text": f"{11-i}위 {description}" if i != 0 else description,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            }
        }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{custom_voice}"
        # url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        response = requests.post(url, json=data, headers=headers)
        if(response.status_code == 200):
            print(f"TTS mp3 for description {i} 저장")
            temp_path = f"temp/speech_{i}.mp3"
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            audio = AudioSegment.from_file(temp_path)
        
            # 오디오 파일의 길이가 5초보다 긴 경우, 속도를 조절
            if len(audio) > 5000:  # 5000ms = 5초
                # 오디오 속도 조절을 위한 배수 계산
                speed_change = (len(audio) / 5000)
                # 속도가 빨라진 오디오 생성
                fast_audio = audio.speedup(playback_speed=speed_change)
                # 속도가 조절된 오디오 파일 저장
                fast_audio.export(f"generated/speech_{i}.mp3", format="mp3")
            else:
                # 오디오 길이가 5초 이하인 경우, 원본 사용
                audio.export(f"generated/speech_{i}.mp3", format="mp3")    

        else:
            print("Error Code:" + str(response.status_code))

    # for i, description in enumerate(descriptions):
    #     # gTTS를 사용하여 오디오 파일 생성
    #     speech = gTTS(text=description, lang='ko', tld='ca', slow=False)
    #     temp_path = f"temp/speech_{i}.mp3"
    #     speech.save(temp_path)
        
    #     # 생성된 오디오 파일 로드
    #     audio = AudioSegment.from_file(temp_path)
        
    #     # 오디오 파일의 길이가 5초보다 긴 경우, 속도를 조절
    #     if len(audio) > 5000:  # 5000ms = 5초
    #         # 오디오 속도 조절을 위한 배수 계산
    #         speed_change = (len(audio) / 5000)
    #         # 속도가 빨라진 오디오 생성
    #         fast_audio = audio.speedup(playback_speed=speed_change)
    #         # 속도가 조절된 오디오 파일 저장
    #         fast_audio.export(f"generated/speech_{i}.mp3", format="mp3")
    #     else:
    #         # 오디오 길이가 5초 이하인 경우, 원본 사용
    #         audio.export(f"generated/speech_{i}.mp3", format="mp3")    
    # for i, description in enumerate(descriptions):
    #     speech = gTTS(text=description, lang='ko', tld='ca', slow=False)
    #     speech.save(f"generated/speech_{i}.mp3")
    # # This code snippet checks if the duration of the audio clip (speech) plus 1.3 seconds exceeds 58
    # seconds. If it does, it prints a message indicating that the speech is too long and provides the
    # duration of the speech and the total duration (speech duration + 1.3 seconds). It then exits the
    # program.
    # if (audio_clip.duration + 1.3 > 58):
    #     print('\nSpeech too long!\n' + str(audio_clip.duration) + ' seconds\n' + str(audio_clip.duration + 1.3) + ' total')
    #     exit()

    # print('\n')
    # 오디오 파일 로드
    # audio = AudioSegment.from_file("generated/speech.mp3", format="mp3")

    # # 오디오 속도 2배로 증가
    # fast_audio = speedup(audio, playback_speed=1.2)

    # # 변경된 오디오 파일 저장
    #

# Create the script file
# 텍스트를 줄 단위로 분리
loaded_script = open('generated/gpt_script.txt', 'r', encoding='utf-8')
content = loaded_script.read()
lines = content.strip().split('\n')


get_youtube_data(playlist_items)
# get_gpt_response(video_info_gpt)
generate_tts()



def generate_final_audio(speech_files_prefix, outro_file, background_music_file, final_audio_file):
    """
    최종 오디오 클립을 생성하고 파일로 저장하는 메서드.
    
    :param speech_files_prefix: 음성 파일명의 접두사 (예: 'generated/speech_')
    :param outro_file: 아웃트로 오디오 파일의 경로
    :param background_music_file: 배경 음악 파일의 경로
    :param final_audio_file: 최종 오디오 파일을 저장할 경로
    """
    # 초기 오디오 세그먼트 생성 (무음으로 시작)
    audio_clip = AudioSegment.silent(duration=0)

    # 생성된 음성 파일들을 순서대로 추가
    for i in range(12):
        speech_segment = AudioSegment.from_file(f"{speech_files_prefix}{i}.mp3")
        audio_clip += speech_segment
        
        # 음성 세그먼트 추가 후 현재 길이 확인
        current_length = len(speech_segment)
        # 현재 길이가 5초 미만이면, 5초가 될 때까지 무음 추가
        if current_length < 5000:
            silence_duration = 5000 - current_length
            audio_clip += AudioSegment.silent(duration=silence_duration)

    # 아웃트로 오디오 추가
    outro_audio = AudioSegment.from_file(outro_file)
    audio_clip += outro_audio

    # 배경 음악 추가 및 조정
    background_music = AudioSegment.from_file(background_music_file)
    background_music -= 10  # 배경 음악 볼륨을 낮춤
    background_music = background_music[:len(audio_clip)]

    # 배경 음악과 음성 클립을 오버레이
    final_audio_clip = audio_clip.overlay(background_music)
    
    # 오디오 클립을 파일로 저장
    final_audio_clip.export(final_audio_file, format="mp3")

# 메서드 사용 예시
generate_final_audio('generated/speech_', 'generated/outro_hong9.mp3', 'generated/hong9_ost.mp3', 'final_audio.mp3')

# 목표 해상도 설정
target_width = 1080
target_height = 1920
target_ratio = 9 / 16

final_clips = []

# 인트로 텍스트 클립 생성
intro_text = "24년 2월 셋째주\n원투차트\n- 예능 유튜브 순위 -"
intro_text_clip = TextClip(intro_text, fontsize=100, color='white', bg_color='transparent', font='aggroB.otf', size=(target_width, target_height)).set_duration(5)
intro_video = VideoFileClip("intro_wantu.mov")

# 인트로 텍스트 클립을 비디오 클립으로 변환 (배경색이 검은색인 텍스트 클립)
intro_clip = CompositeVideoClip([intro_video,intro_text_clip], size=(target_width, target_height))
# 인트로 클립을 final_clips 리스트의 첫 번째 요소로 추가
final_clips.insert(0, intro_clip)
# 나머지 비디오 처리 로직은 동일하게 유지
# ...

# 모든 클립을 하나의 비디오로 병합
final_clip = concatenate_videoclips(final_clips)

for video in videos_info:
    # 비디오 클립 로드 및 크기 조정
    video_clip = VideoFileClip(video['video_path'])
    original_ratio = video_clip.w / video_clip.h
    # 목표 비율에 맞게 비디오 클립 조정
    # if original_ratio > target_ratio:
    #     # 원본 비디오가 목표 비율보다 넓은 경우, 너비를 조정
    new_height = video_clip.h
    new_width = int(new_height * target_ratio)
    video_clip = video_clip.crop(x_center=video_clip.w/2, width=new_width)
    # else:
        # 원본 비디오가 목표 비율보다 높은 경우, 높이를 조정
    # new_width = video_clip.w
    # new_height = int(new_width / target_ratio)
    # video_clip = video_clip.crop(y_center=video_clip.h/2, height=new_height)

    # 최종 비디오 크기를 목표 해상도로 조정
    video_clip = video_clip.resize(width=target_width, height=target_height)


    # 썸네일 이미지로부터 ImageClip 생성 및 크기 조정
    thumbnail_clip = ImageClip(video['thumbnail']).set_duration(3).resize(width=target_width)  # 썸네일 크기를 비디오 높이의 1/3로 조정
    # 썸네일을 비디오 중앙에 위치시킴
    thumbnail_clip = thumbnail_clip.set_position(("center", "center"))
    
    # 비디오 제목으로 TextClip 생성
    if len(video['title']) > 30:
        # 제목을 30자로 자르고 '...'을 추가
        shortened_title = video['title'][:27] + '...'
    else:
        shortened_title = video['title']

    # 줄바꿈을 위해 제목을 wrap 함수로 처리
    wrapped_title = wrap(shortened_title, 10)
    formatted_title = "\n".join(wrapped_title)  # 각 줄을 개행 문자로 연결하여 하나의 문자열로 만듦    
    txt_clip = TextClip(formatted_title, fontsize=70, color='white', bg_color='black', font='aggroB.otf').set_position('bottom').set_duration(5)
    rank_text = TextClip(f"{10- videos_info.index(video) }위", fontsize=300, color='white', bg_color='transparent', font='aggroB.otf').set_position('top').set_duration(5)


    # 검은색 배경 클립 생성
    # 여기서는 텍스트 클립의 높이를 예상하여 설정해야 합니다. 예를 들어, 텍스트 클립의 높이가 100px라고 가정합니다.
    black_background_clip = ColorClip(size=(target_width, 400), color=(0,0,0)).set_duration(5)

    # 검은색 배경 클립을 비디오 하단에 위치시키기
    black_background_clip = black_background_clip.set_position(("center", "bottom"))
    text_on_black_clip = CompositeVideoClip([black_background_clip, txt_clip.set_position(("center", "center"))])
    # 썸네일 위에 텍스트 제목을 오버레이
    composite_clip = CompositeVideoClip([video_clip, thumbnail_clip, text_on_black_clip.set_position(("center", "bottom")), rank_text])  # 비디오 클립에 썸네일과 텍스트 클립을 오버레이
    
    # 썸네일/제목 클립과 비디오 클립을 순서대로 리스트에 추가
    final_clips.append(composite_clip)

# 모든 클립을 하나의 비디오로 병합
final_clip = concatenate_videoclips(final_clips)

# 비디오의 원래 크기를 가져옵니다
w, h = final_clip.size

# 목표 비율 설정 (9:16)
current_ratio = w / h

# 현재 비디오 비율이 목표 비율보다 넓은 경우, 너비를 조정합니다
if current_ratio > target_ratio:
    # 새 너비 계산
    new_width = int(h * target_ratio)
    # 비디오를 중앙에서 자릅니다
    final_clip = final_clip.crop(x_center=w/2, width=new_width)

# 현재 비디오 비율이 목표 비율보다 좁은 경우, 높이를 조정합니다
else:
    # 새 높이 계산
    new_height = int(w / target_ratio)
    # 비디오를 중앙에서 자릅니다
    final_clip = final_clip.crop(y_center=h/2, height=new_height)

# 최종 비디오를 목표 해상도로 리사이즈합니다
final_clip = final_clip.resize(newsize=(target_width, target_height))

# 최종 비디오에 오디오 클립 추가 및 파일 저장
final_clip = concatenate_videoclips(final_clips)
final_clip_audio = AudioFileClip("final_audio.mp3")
final_clip = final_clip.set_audio(final_clip_audio)
final_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")