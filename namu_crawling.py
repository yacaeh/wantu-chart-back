from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from selenium.webdriver.common.by import By

# brew 로 설치된 chromedriver의 path (Mac)
path = "/opt/homebrew/bin/chromedriver"

# 윈도우용 크롬 웹드라이버 실행 경로 (Windows)
excutable_path = "chromedriver.exe"
name = "머니게임(웹예능)"
# 크롤링할 사이트 주소를 정의합니다.
source_url = "https://namu.wiki/w/" + name

# 사이트의 html 구조에 기반하여 크롤링을 수행합니다.
driver = webdriver.Chrome()
# driver = webdriver.Chrome(executable_path=excutable_path)  # for Windows
driver.get(source_url)
print("+" * 100)
print(driver.title)
print(driver.current_url)
print("킹무위키 크롤링")
print("-" * 100)

time.sleep(2)

allProfileElement = driver.find_element(By.CSS_SELECTOR, 
    "div.wiki-table-wrap.table-right")

try:
    # allYoutubeVideos = WebDriverWait(driver,10).until(
    #  EC.presence_of_element_located((By.XPATH, "//*[@id='video-title']"))
    # )
    driver.implicitly_wait(120)
    allYoutubeVideos = driver.find_elements(By.XPATH, "//*[@id='video-title']")

finally:
    f.close()
    driver.quit()
