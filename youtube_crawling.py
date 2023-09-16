from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import requests
from pytube import extract
from pytube import YouTube

search = "우마게임"
channel = "@physicalgallery_official"
# channel = "@koreanzombie"
# 크롤링할 사이트 주소를 정의합니다.
source_url = "https://www.youtube.com/" + channel + "/search?query=" + search

# 사이트의 html 구조에 기반하여 크롤링을 수행합니다.
driver = webdriver.Chrome()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.get(source_url)

print("+" * 100)
print(driver.title)
print(driver.current_url)
print("-" * 100)

time.sleep(2)

f = open(f'{search}.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(['title', 'id', 'views', 'length', 'description', 'thumbnail_url', 'publishedAt', 'tags', 'categoryId'])
try:
    # allYoutubeVideos = WebDriverWait(driver,10).until(
    #  EC.presence_of_element_located((By.XPATH, "//*[@id='video-title']"))
    # )
    driver.implicitly_wait(180)
    allYoutubeVideos = driver.find_elements(By.XPATH, "//*[@id='video-title']")
    for element in allYoutubeVideos:
        # print("Without filter")
        # print(element.text)
        # print(element.get_attribute("href"))

        if ("EP" or "ep" or "Ep" or "화") and search in element.text:
            print("With filter")
            print(element.text)
            print(element.get_attribute("href"))
            if element.get_attribute("href") is not None:
                response = requests.get(f"https://yt.lemnoslife.com/noKey/videos?part=snippet&id={extract.video_id(element.get_attribute('href'))}")
                print(response.json()['items'][0])
                yt = YouTube(element.get_attribute("href"))

                title = response.json()['items'][0]['snippet']['title']
                id = response.json()['items'][0]['id']
                description = response.json()['items'][0]['snippet']['description']
                thumbnail = response.json()['items'][0]['snippet']['thumbnails']['default']['url']
                channelTitle = response.json()['items'][0]['snippet']['channelTitle']
                publishedAt = response.json()['items'][0]['snippet']['publishedAt']

                try:
                    tags = ','.join(response.json()['items'][0]['snippet']['tags'])
                except KeyError:
                    tags = None
                categoryId = response.json()['items'][0]['snippet']['categoryId']
                views = yt.views
                length = yt.length

                print("Title:",title)
                print("Id:",id)
                print("description:",description)
                print("thumbnail:", thumbnail)
                print("channelTitle:",channelTitle)
                print("PublishedAt:", publishedAt)
                print("tags:", tags)
                print("CategoryId:" , categoryId)
                print("Views:", views)
                print("Length:", length)
                
                wr.writerow([title, id, views, length, description, thumbnail, publishedAt,tags,categoryId])
    
    print("allYoutubeVideos")

finally:
    f.close()
    driver.quit()


# https://yt.lemnoslife.com/videos?part=mostReplayed&id=Dg2sRxQyXfM
# https://yt.lemnoslife.com/noKey/videos?part=snippet&id=Dg2sRxQyXfM