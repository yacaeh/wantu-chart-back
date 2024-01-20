import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
import time
from datetime import datetime
from googleapiclient.discovery import build #pip install google-api-python-client 필요
import requests
from app.settings import TIME_ZONE, SCHEDULER_CONFIG
from apscheduler.triggers.cron import CronTrigger
import csv
import os
from googleapiclient.errors import HttpError
from movies.models import Movie, Episode, DailyView, DailyRank, WeeklyRank, MonthlyRank, Genre, Rating
from app.utils.youtube import get_channel_info, get_video_details, get_highlights, make_video_info_request, make_api_request, get_video_ids, process_playlist, API_KEY_LIST, API_INDEX,add_playlist_videos
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import random
from users.models import User
import string
from app.utils.utils import add_allowlist, send_email
# AIzaSyC9NVqk0XjmU3BP26njxMJoQWmmg0IjlJQ
# AIzaSyDlo1ez9E0Zh81kij8v4Ipx0NWVRrocx0w
# AIzaSyDHABt7h3oLJiC64F3QPdBt8DKY7BwDckw
logger = logging.getLogger(__name__)


def load_youtuber_names():
    with open('youtuber_names.txt', 'r') as file:
        names = [name.strip() for name in file.readlines()]
    return names
random_youtubers = load_youtuber_names()

def random_username():
    """랜덤한 형용사와 명사를 조합하여 사용자 이름을 생성하는 함수입니다."""
    adjectives = ['가냘픈', '가는', '가엾은', '가파른', '같은', '거센', '거친', '검은', '게으른', '고달픈', '고른', '고마운', '고운', '고픈', '곧은', '괜찮은', '구석진', '굳은', '굵은', '귀여운', '그런', '그른', '그리운', '기다란', '기쁜', '긴', '깊은', '깎아지른', '깨끗한', '나쁜', '나은', '난데없는', '날랜', '날카로운', '낮은', '너그러운', '너른', '널따란', '넓은', '네모난', '노란', '높은', '누런', '눅은', '느닷없는', '느린', '늦은', '다른', '더러운', '더운', '덜된', '동그란', '돼먹잖은', '된', '둥그런', '둥근', '뒤늦은', '드문', '딱한', '때늦은', '뛰어난', '뜨거운', '막다른', '많은', '매운', '먼', '멋진', '메마른', '메스꺼운', '모난', '못난', '못된', '못생긴', '무거운', '무딘', '무른', '무서운', '미끄러운', '미운', '바람직한', '반가운', '밝은', '밤늦은', '보드라운', '보람찬', '부드러운', '부른', '붉은', '비싼', '빠른', '빨간', '뻘건', '뼈저린', '뽀얀', '뿌연', '새로운', '서툰', '섣부른', '설운', '성가신', '센', '수줍은', '쉬운', '스스러운', '슬픈', '시원찮은', '싫은', '싼', '쌀쌀맞은', '쏜살같은', '쓰디쓴', '쓰린', '쓴', '아니꼬운', '아닌', '아름다운', '아쉬운', '아픈', '안된', '안쓰러운', '안타까운', '않은', '알맞은', '약빠른', '약은', '얇은', '얕은', '어두운', '어려운', '어린', '언짢은', '엄청난', '없는', '여문', '열띤', '예쁜', '올바른', '옳은', '외로운', '우스운', '의심스런', '이른', '익은', '있는', '작은', '잘난', '잘빠진', '잘생긴', '재미있는', '적은', '젊은', '점잖은', '조그만', '좁은', '좋은', '주제넘은', '줄기찬', '즐거운', '지나친', '지혜로운', '질긴', '짓궂은', '짙은', '짠', '짧은', '케케묵은', '큰', '탐스러운', '턱없는', '푸른', '한결같은', '흐린', '희망찬', '흰', '힘겨운']
    return '_'.join([random.choice(adjectives), random.choice(random_youtubers)])

def random_email():
    # Generate a random username (5~10 characters)
    username_length = random.randint(5, 10)
    username = ''.join(random.choice(string.ascii_letters) for _ in range(username_length))

    # Append '@example.com' to the username to create an email address
    email_address = username + '@gmail.com'
    return email_address

def create_test_users(n=10):
    """n개의 테스트용 유저를 생성하는 함수입니다."""
    for _ in range(n):
        print(random_username())
        User.objects.create(
            name=random_username(),
            email= random_email(),
            password='testpassword',
            google_token='testtoken',
            introduction='testintro',
        )

def get_or_create_csv(file_path, header):
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        # File already exists, no need to create a new one
        pass

def update_review_sample():
    # Get Users
    users = User.objects.filter(google_token='testtoken')
    # 사용하려는 API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # 인증정보 파일을 통한 인증
    credentials = ServiceAccountCredentials.from_json_keyfile_name('IAM.json', scope)

    gc = gspread.authorize(credentials)

    # 구글 스프레드시트의 이름
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1-1j55mkrY_Tyi8K2TT9eGJiRA1wcychZIbOC5kOoUoQ/edit#gid=1600710680'

    # 스프레드시트 열기
    doc = gc.open_by_url(spreadsheet_url)
    # a 시트 불러오기
    worksheet = doc.get_worksheet(6)
    # 모든 데이터 가져오기
    data = worksheet.get_all_values()
    data = data[1:]
    reviews = []
    pattern = r'(.*)\/([0-9.]+)'


    for item in data:
        print(item[15])
        if item[14] != '완료':
            playlist = item[5]
            review1 = item[9]
            review2 = item[10]
            review3 = item[11]
            review4 = item[12]
            review5 = item[13]

            if review1 != '':
              reviews.append(review1)
            
            if review2 != '':
              reviews.append(review2)
            
            if review3 != '':
              reviews.append(review3)
            
            if review4 != '':             
              reviews.append(review4)

            if review5 != '':    
              reviews.append(review5)
            
            for review in reviews:
                print(review)
                user = random.choice(users)
                comment, rating = review.split('/')
                rating = float(rating)

                try:
                    Rating.objects.create(user=user, movie=Movie.objects.filter(playlist=playlist)[0], rate=rating, comment=comment, spoiler=False)

                except KeyError:
                    print("ERROR")
                    
            # Update status
            worksheet.update_acell('O'+str(data.index(item)+2), '완료')
                        

def update_googlesheet():
    # 사용하려는 API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # 인증정보 파일을 통한 인증
    credentials = ServiceAccountCredentials.from_json_keyfile_name('IAM.json', scope)

    gc = gspread.authorize(credentials)

    # 구글 스프레드시트의 이름
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1-1j55mkrY_Tyi8K2TT9eGJiRA1wcychZIbOC5kOoUoQ/edit#gid=1600710680'

    # 스프레드시트 열기
    doc = gc.open_by_url(spreadsheet_url)
    # a 시트 불러오기
    worksheet = doc.get_worksheet(6)
    # 모든 데이터 가져오기
    data = worksheet.get_all_values()
    data = data[1:]
    for item in data:
        if item[0] != '완료':
            playlistName = item[1]
            description = item[2]
            publishedAt = item[3]
            trailer = item[4]
            playlist = item[5]
            genre = item[6]

            poster_image = "https://i.ytimg.com/vi/"+trailer+"/hqdefault.jpg"
            cleaned_text = re.sub("[0-9. ]", "", genre)
            try:
                new_movie = Movie.objects.get(title=playlistName, trailer=trailer, playlist=playlist)
                print("movie already exists")
                worksheet.update_acell('A'+str(data.index(item)+2), '완료')
                continue


            # instances.append(Movie(title=playlistName, trailer=trailer, playlist=playlist, poster_image=poster_image, channel=channel, release_date=publishedAt, description=description))
            except Movie.DoesNotExist:
                new_movie = Movie.objects.create(title=playlistName, trailer=trailer, playlist=playlist, poster_image=poster_image,  description=description)
                new_id = new_movie.pk
                if genre != '':
                  genre, created = Genre.objects.get_or_create(name=genre)
                  new_movie.genre.add(genre)
                  print("Genre added to movie", genre.name)
                new_movie.genre.through.objects.update_or_create(movie_id=new_id, genre_id=genre.pk)
                print(playlist, cleaned_text)
                add_playlist_videos(playlist, True)
                worksheet.update_acell('A'+str(data.index(item)+2), '완료')
            except Movie.MultipleObjectsReturned:
                print("Multiple objects returned")
                worksheet.update_acell('A'+str(data.index(item)+2), '완료')

   

def save_data_to_csv(file_path, data):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

csv_folder = 'static/logs'
# Example usage


def my_daily_job(index=0):
    print("Are you working?")
    now = datetime.now()
    global API_KEY
    global API_INDEX

    # 현재 날짜를 년, 월, 일로 분리
    year = now.year
    month = now.month
    day = now.day
    print(f"오늘의 날짜: {year}년 {month}월 {day}일")
    movies = Movie.objects.all()
    movies_playlist=[movie.playlist for movie in movies]
    
    if (index != 0):
        print("CUT!", index)
        movies_playlist = movies_playlist[index:]
        print(len(movies_playlist))

    print(len(movies_playlist))

    for playlist in movies_playlist:
        add_playlist_videos(playlist)
def my_job_a():
  my_daily_job()
  # 실행시킬 Job
  # 여기서 정의하지 않고, import 해도 됨

  pass
  
def my_job_b():
  # 실행시킬 Job
  # 여기서 정의하지 않고, import 해도 됨
  # update ranks or daily scores 
  # update daily scores 
  # 조회수 + 좋아요 수 (10) + 댓글 수 (5) + 싫어요 수 (-15)
  # Rank table


  pass

def start():
  print("START>>>>!")
  # def handle(self, *args, **options):
  scheduler = BackgroundScheduler(timezone=TIME_ZONE) # BlockingScheduler를 사용할 수도 있습니다.
  scheduler.add_jobstore(DjangoJobStore(), "default") 
  email = 'yoonseok@wantu.io'
  # add_allowlist(email)
  # send_email(email, '경인', '원투차트 주간 콘텐츠 업데이트 알림')
  # my_job_a() # 한번 실행해주고 시작합니다.
  # update_googlesheet()
  # create_test_users(100)
  update_review_sample()
  scheduler.add_job(
    my_job_a,
    trigger=CronTrigger(hour='12'),  # 12시 마다 작동합니다.
    id="my_job",  # id는 고유해야합니다. 
    max_instances=1,
    replace_existing=True,
  )
  print("Added job 'my_job_a'.")

  # scheduler.add_job(
  #   my_job_b,
  #   trigger=CronTrigger(
  #     hour="03", minute="00"
  #   ),  # 실행 시간입니다. 여기선 매주 월요일 3시에 실행합니다.
  #   id="my_job_b",
  #   max_instances=1,
  #   replace_existing=True,
  # )
  # logger.info("Added job 'my_job_b'.")

  try:
    logger.info("Starting scheduler...")
    scheduler.start() # 없으면 동작하지 않습니다.
  except KeyboardInterrupt:
    logger.info("Stopping scheduler...")
    scheduler.shutdown()
    logger.info("Scheduler shut down successfully!")
