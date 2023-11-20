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
from movies.models import Movie, Episode, DailyView, DailyRank, WeeklyRank, MonthlyRank
from app.utils.youtube import get_channel_info, get_video_details, get_highlights, make_video_info_request, make_api_request, get_video_ids, process_playlist, API_KEY_LIST, API_INDEX,add_playlist_videos
# AIzaSyC9NVqk0XjmU3BP26njxMJoQWmmg0IjlJQ
# AIzaSyDlo1ez9E0Zh81kij8v4Ipx0NWVRrocx0w
# AIzaSyDHABt7h3oLJiC64F3QPdBt8DKY7BwDckw
logger = logging.getLogger(__name__)

def get_or_create_csv(file_path, header):
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
    else:
        # File already exists, no need to create a new one
        pass

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
#   my_daily_job(422)
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

  my_job_a() # 한번 실행해주고 시작합니다.
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
