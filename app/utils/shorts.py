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
import uuid
from datetime import datetime
import random


class VideoCreator:
    def __init__(self, title, videos_info, voice_id, intro_text, outro_text, background_mp3, intro_video_file, outro_video_file):
        self.title = title
        self.videos_info = videos_info
        self.target_width = 1080
        self.target_height = 1920
        self.target_ratio = 9 / 16
        self.intro_text = intro_text
        self.outro_text = outro_text
        self.background_mp3 = background_mp3
        self.intro_video_file = intro_video_file
        self.outro_video_file = outro_video_file
        self.video_info_gpt = []
        self.voice_id = voice_id

        self.YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]

    @staticmethod
    def generate_uid_with_date():
        # 현재 날짜와 시간을 'YYYYMMDDHHMMSS' 형식의 문자열로 변환
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        # 4자리 랜덤 숫자 생성
        random_str = random.randint(1000, 9999)
        # 날짜 문자열과 랜덤 숫자를 결합하여 UID 생성
        uid = f"{date_str}{random_str}"
        return uid
    # 특수 문자와 이모지를 제거하는 함수
    @staticmethod
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
    @staticmethod
    def download_and_save_thumbnail(url, save_path):
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(save_path)

    @staticmethod
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
    
    @staticmethod        
    def get_youtube_id_from_url(url):
        print("Print from get_youtube_id_from_url", url)
        """
        YouTube URL에서 비디오 ID를 추출하는 메서드
        :param url: YouTube 비디오 URL
        :return: 추출된 YouTube 비디오 ID
        """
        # YouTube URL에서 비디오 ID를 추출하기 위한 정규 표현식
        video_id_match = re.search(r"(?<=v=)[^&#]+", url)
        video_id_match = video_id_match or re.search(r"(?<=be/)[^&#]+", url)
        video_id_match = video_id_match or re.search(r"(?<=embed/)[^&#]+", url)

        video_id = video_id_match.group(0) if video_id_match else None
        return video_id
    # 비디오 다운로드 함수
    @staticmethod
    def download_video(video_id, filename):
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        # 현재 작업 디렉토리에 지정된 파일 이름으로 비디오 저장
        stream.download(filename=filename)

        save_path = 'youtube_rank_videos'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    @staticmethod
    def get_video_details(video_id, api_key):
        video_details_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet&key={api_key}"
        response = requests.get(video_details_url)
        video_details = response.json()
        return video_details

    @staticmethod
    def get_youtube_data(self):
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
            self.download_and_save_thumbnail(video_thumbnail, thumbnail_path)

            output_path = save_path+'/'+video_id+'_extracted.mp4'
            self.videos_info.append({
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

    @staticmethod
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

    # Create the directory
    if os.path.exists('generated') == False:
        os.mkdir('generated')


    def generate_tts(self):
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

    def elevenlabs_tts(self, description, voice_id, path):
        CHUNK_SIZE = 1024
        headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.environ["ELEVENLABS_API"]
        }
        
        data = {
            "text": description,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            }
        }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        # url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        response = requests.post(url, json=data, headers=headers)
        
        if(response.status_code == 200):
            print(f"TTS mp3 for description {path} 저장")
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            audio = AudioSegment.from_file(path)
        
            # 오디오 파일의 길이가 5초보다 긴 경우, 속도를 조절
            if len(audio) > 5000:  # 5000ms = 5초
                # 오디오 속도 조절을 위한 배수 계산
                speed_change = (len(audio) / 5000)
                # 속도가 빨라진 오디오 생성
                fast_audio = audio.speedup(playback_speed=speed_change)
                # 속도가 조절된 오디오 파일 저장
                fast_audio.export(path, format="mp3")
            else:
                # 오디오 길이가 5초 이하인 경우, 원본 사용
                audio.export(path, format="mp3")    

        else:
            print("Error Code:" + str(response.status_code))


    @staticmethod
    def generate_final_audio(number_of_tracks, speech_files_prefix, intro_file, outro_file, background_music_file, final_audio_file):
        """
        최종 오디오 클립을 생성하고 파일로 저장하는 메서드.
        
        :param speech_files_prefix: 음성 파일명의 접두사 (예: 'generated/speech_')
        :param outro_file: 아웃트로 오디오 파일의 경로
        :param background_music_file: 배경 음악 파일의 경로
        :param final_audio_file: 최종 오디오 파일을 저장할 경로
        """
        # 초기 오디오 세그먼트 생성 (무음으로 시작)
        audio_clip = AudioSegment.silent(duration=0)
        intro_audio = AudioSegment.from_file(intro_file)
        intro_audio_length = len(intro_audio)
        print("intro_audio_length", intro_audio_length)
        if intro_audio_length < 5000:
            silence_duration = 5000 - intro_audio_length
            intro_audio += AudioSegment.silent(duration=silence_duration)
        print("intro_audio_length after", len(intro_audio))
        audio_clip += intro_audio

        # 생성된 음성 파일들을 순서대로 추가
        for i in range(number_of_tracks):
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


    def create_final_video(self):
        target_width = 1080
        target_height = 1920
        target_ratio = 9 / 16

        final_clips = []

        # 인트로 텍스트 클립 생성
        intro_text = self.title
        wrapped_intro_text = wrap(intro_text, 10)
        formatted_intro_text = "\n".join(wrapped_intro_text)

        intro_text_clip = TextClip(formatted_intro_text, fontsize=100, color='white', bg_color='transparent', font='aggroB.otf', size=(target_width, target_height)).set_duration(5)
        intro_video = VideoFileClip(self.intro_video_file).resize(width=target_width, height=target_height)

        # 인트로 텍스트 클립을 비디오 클립으로 변환 (배경색이 검은색인 텍스트 클립)
        intro_clip = CompositeVideoClip([intro_video,intro_text_clip], size=(target_width, target_height))
        # 인트로 클립을 final_clips 리스트의 첫 번째 요소로 추가
        final_clips.insert(0, intro_clip)

        # 모든 클립을 하나의 비디오로 병합
        final_clip = concatenate_videoclips(final_clips)

        for video in self.videos_info:
            # 비디오 클립 로드 및 크기 조정
            video_clip = VideoFileClip(video['video_path'])
            original_ratio = video_clip.w / video_clip.h
            new_height = video_clip.h
            new_width = int(new_height * target_ratio)
            video_clip = video_clip.crop(x_center=video_clip.w/2, width=new_width)

            # 최종 비디오 크기를 목표 해상도로 조정
            video_clip = video_clip.resize(width=target_width, height=target_height)

            # 썸네일 이미지로부터 ImageClip 생성 및 크기 조정
            thumbnail_clip = ImageClip(video['thumbnail']).set_duration(3).resize(width=target_width)
            thumbnail_clip = thumbnail_clip.set_position(("center", "center"))
            
            # 비디오 제목으로 TextClip 생성
            if len(video['title']) > 30:
                shortened_title = video['title'][:27] + '...'
            else:
                shortened_title = video['title']

            wrapped_title = wrap(shortened_title, 10)
            formatted_title = "\n".join(wrapped_title)    
            txt_clip = TextClip(formatted_title, fontsize=70, color='white', bg_color='black', font='aggroB.otf').set_position('bottom').set_duration(5)
            rank_text = TextClip(f"{10- self.videos_info.index(video) }위", fontsize=300, color='white', bg_color='transparent', font='aggroB.otf').set_position('top').set_duration(5)

            black_background_clip = ColorClip(size=(target_width, 400), color=(0,0,0)).set_duration(5)
            black_background_clip = black_background_clip.set_position(("center", "bottom"))
            text_on_black_clip = CompositeVideoClip([black_background_clip, txt_clip.set_position(("center", "center"))])
            composite_clip = CompositeVideoClip([video_clip, thumbnail_clip, text_on_black_clip.set_position(("center", "bottom")), rank_text])
            
            final_clips.append(composite_clip)

        # Add outro video
        # Add outro textclip
        outro_text = self.outro_text
        wrapped_outro_text = wrap(outro_text, 10)
        formatted_outro_text = "\n".join(wrapped_outro_text)
        print("self.outro_video_file", self.outro_video_file)
        # outro_text_clip = TextClip(formatted_outro_text, fontsize=100, color='white', bg_color='transparent', font='aggroB.otf', size=(target_width, target_height)).set_duration(5)
        outro_video = VideoFileClip(self.outro_video_file).resize(width=target_width, height=target_height)
        # outro_clip = CompositeVideoClip([outro_video,outro_text_clip], size=(target_width, target_height))
        final_clips.append(outro_video)
        final_clip = concatenate_videoclips(final_clips)

        w, h = final_clip.size
        current_ratio = w / h

        if current_ratio > target_ratio:
            new_width = int(h * target_ratio)
            final_clip = final_clip.crop(x_center=w/2, width=new_width)
        else:
            new_height = int(w / target_ratio)
            final_clip = final_clip.crop(y_center=h/2, height=new_height)
    
        final_clip = final_clip.resize(newsize=(target_width, target_height))

        final_clip_audio = AudioFileClip("final_audio.mp3")
        final_clip = final_clip.set_audio(final_clip_audio)
        final_clip.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")

    def get_custom_voice(self, name, description, voice_id):
        CHUNK_SIZE = 1024
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": os.environ["ELEVENLABS_API"]
        }
        
        data = {
            "text": description,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            }
        }

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        response = requests.post(url, json=data, headers=headers)
        if(response.status_code == 200):
            print(f"TTS mp3 for description 저장")
            temp_path = f"temp/{name}.mp3"
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            audio = AudioSegment.from_file(temp_path)
        
            # 오디오 파일의 길이가 5초보다 긴 경우, 속도를 조절
            if len(audio) > 5000:
                # 오디오 속도 조절을 위한 배수 계산
                speed_change = (len(audio) / 5000)
                # 속도가 빨라진 오디오 생성
                fast_audio = audio.speedup(playback_speed=speed_change)
                # 속도가 조절된 오디오 파일 저장
                fast_audio.export(f"generated/{name}.mp3", format="mp3")
            else:
                # 오디오 길이가 5초 이하인 경우, 원본 사용
                audio.export(f"generated/{name}.mp3", format="mp3")

    def generate_video_process(self):
        # Create the script file
        # 텍스트를 줄 단위로 분리
        # get_gpt_response(video_info_gpt)
        # download the videos

        for index, video in enumerate(self.videos_info):
            self.download_video(video['id'], video['id']+'.mp4')
            video_path = video['id']+'.mp4'
            save_path = 'youtube_rank_videos'
            output_path = save_path+'/'+video['id']+'_extracted.mp4'
            # 예시 사용법
            start_time = 10  # 시작 시간 (10초)
            end_time = 15  # 종료 시간 (15초)

            # 함수 호출
            self.extract_and_save_clip(video_path, start_time, end_time, output_path)
            # 원본 비디오 파일 삭제
            os.remove(video_path)
            description = f"{len(self.videos_info.length)-index}위 {video['title'] + video['description']}"
            self.get_custom_voice(f"speech_{index}",description, self.voice_id)

        # 메서드 사용 예시
        self.generate_final_audio('generated/speech_', 'generated/outro_hong9.mp3', 'generated/hong9_ost.mp3', 'final_audio_hong9.mp3')

    def combine_video_audio(self, audio_path, output_path):
        # 비디오 파일 로드
        # 비디오에 오디오 추가
        target_width = 1080
        target_height = 1920
        target_ratio = 9 / 16

        final_clips = []

        # 인트로 텍스트 클립 생성
        intro_text = self.title
        intro_text_clip = TextClip(intro_text, fontsize=100, color='white', bg_color='transparent', font='aggroB.otf', size=(target_width, target_height)).set_duration(5)
        intro_video = VideoFileClip(self.intro_video_file).resize(width=target_width, height=target_height)
        intro_duration = intro_video.duration
        print("Intro duration:", intro_duration)
        if intro_duration > 5:
            # 인트로 비디오가 5초보다 길 경우, 처음 5초만 잘라냄
            intro_video = intro_video.subclip(0, 5)
        elif intro_duration < 5:
            # 인트로 비디오가 5초보다 짧을 경우, 비디오를 반복하여 5초 동안 재생
            repeats = int(5 // intro_duration) + 1  # 필요한 반복 횟수 계산
            intro_video = concatenate_videoclips([intro_video] * repeats).subclip(0, 5)

        # 인트로 텍스트 클립을 비디오 클립으로 변환 (배경색이 검은색인 텍스트 클립)
        intro_clip = CompositeVideoClip([intro_video,intro_text_clip], size=(target_width, target_height))
        # 인트로 클립을 final_clips 리스트의 첫 번째 요소로 추가
        final_clips.insert(0, intro_clip)

        # 모든 클립을 하나의 비디오로 병합
        final_clip = concatenate_videoclips(final_clips)
        for index, video in enumerate(self.videos_info):
            # 비디오 클립 로드 및 크기 조정
            video_id = self.get_youtube_id_from_url(self.videos_info[video]['url'])
            video_clip = VideoFileClip(f'temp/{video_id}_extracted.mp4')
            new_height = video_clip.h
            new_width = int(new_height * target_ratio)
            video_clip = video_clip.crop(x_center=video_clip.w/2, width=new_width)

            # 최종 비디오 크기를 목표 해상도로 조정
            video_clip = video_clip.resize(width=target_width, height=target_height)

            # 썸네일 이미지로부터 ImageClip 생성 및 크기 조정
            thumbnail_clip = ImageClip(f'temp/{video_id}.jpg').set_duration(3).resize(width=target_width)
            thumbnail_clip = thumbnail_clip.set_position(("center", "center"))
            
            # 비디오 제목으로 TextClip 생성
            if len(self.videos_info[video]['title']) > 30:
                shortened_title = self.videos_info[video]['title'][:27] + '...'
            else:
                shortened_title = self.videos_info[video]['title']

            wrapped_title = wrap(shortened_title, 10)
            formatted_title = "\n".join(wrapped_title)    
            txt_clip = TextClip(formatted_title, fontsize=70, color='white', bg_color='black', font='aggroB.otf').set_position('bottom').set_duration(5)
            rank_text = TextClip(f"{len(self.videos_info)-index }위", fontsize=300, color='white', bg_color='transparent', font='aggroB.otf').set_position('top').set_duration(5)

            black_background_clip = ColorClip(size=(target_width, 400), color=(0,0,0)).set_duration(5)
            black_background_clip = black_background_clip.set_position(("center", "bottom"))
            text_on_black_clip = CompositeVideoClip([black_background_clip, txt_clip.set_position(("center", "center"))])
            composite_clip = CompositeVideoClip([video_clip, thumbnail_clip, text_on_black_clip.set_position(("center", "bottom")), rank_text])
            
            final_clips.append(composite_clip)

        outro_text = self.outro_text
        wrapped_outro_text = wrap(outro_text, 10)
        formatted_outro_text = "\n".join(wrapped_outro_text)
        print("self.outro_video_file", self.outro_video_file)
        # outro_text_clip = TextClip(formatted_outro_text, fontsize=100, color='white', bg_color='transparent', font='aggroB.otf', size=(target_width, target_height)).set_duration(5)
        outro_video = VideoFileClip(self.outro_video_file).resize(width=target_width, height=target_height)
        # outro_clip = CompositeVideoClip([outro_video,outro_text_clip], size=(target_width, target_height))
        final_clips.append(outro_video)
        final_clip = concatenate_videoclips(final_clips)


        final_clip = concatenate_videoclips(final_clips)

        w, h = final_clip.size
        current_ratio = w / h

        if current_ratio > target_ratio:
            new_width = int(h * target_ratio)
            final_clip = final_clip.crop(x_center=w/2, width=new_width)
        else:
            new_height = int(w / target_ratio)
            final_clip = final_clip.crop(y_center=h/2, height=new_height)

        final_clip = final_clip.resize(newsize=(target_width, target_height))

        final_clip_audio = AudioFileClip(audio_path)
        final_clip = final_clip.set_audio(final_clip_audio)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        # 최종 비디오 파일로 저장


    # 비디오 생성
    def create_video(self):
        # 비디오 다운로드 및 썸네일 저장

        # Create intro video
        # generate intro tts
        # generate random uid
        uid = self.generate_uid_with_date()
        # create directory with uid    
        project_dir = f"shorts_output/"
        print("self.intro_text", self.intro_text)
        self.elevenlabs_tts(self.intro_text, self.voice_id, "temp/intro.mp3")

        for idx, video in enumerate(self.videos_info):
            # download Video and save thumbnail
            video_url = ""+self.videos_info[video]['url']
            video_id = self.get_youtube_id_from_url(video_url)
            description = f"{len(self.videos_info)-idx}위 {self.videos_info[video]['title']} {self.videos_info[video]['subtitle']}"
            print("video_id", video_id)
            self.download_video(video_id, f'temp/{video_id}.mp4')
            # get only part of video and remove original
            self.extract_and_save_clip(f'temp/{video_id}.mp4', 10, 15, f'temp/{video_id}_extracted.mp4')
            self.download_and_save_thumbnail(f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg', f"temp/{video_id}.jpg")
            # remove original video
            os.remove(f'temp/{video_id}.mp4')
            # generate tts for each video
            self.elevenlabs_tts(description,self.voice_id, f"temp/speech_{idx}.mp3")

            # generate video process
        self.elevenlabs_tts(self.outro_text,self.voice_id, "temp/outro.mp3")
        self.generate_final_audio(len(self.videos_info),'temp/speech_',"temp/intro.mp3", 'temp/outro.mp3', f'{self.background_mp3}', f'shorts_output/{uid}_final_audio.mp3')
        self.combine_video_audio(f'shorts_output/{uid}_final_audio.mp3', f'shorts_output/{uid}_final_video.mp4')

        return True