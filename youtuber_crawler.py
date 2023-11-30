import requests
from bs4 import BeautifulSoup
import re

def get_youtuber_names(n=9):
    names = []
    for i in range(n):
        url = f"https://youtube-rank.com/board/bbs/board.php?bo_table=youtube&page={i+1}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        channel_list = soup.select('form > table > tbody > tr > td.subject > h1 > a')
        for channel in channel_list:
            # Remove spaces and special characters from the name
            name = re.sub(r'\W+', '', channel.text.strip())
            if len(name) <= 10:
                names.append(name)
        
    return names

youtuber_names = get_youtuber_names(20)

with open('youtuber_names.txt', 'w') as file:
    for name in youtuber_names:
        file.write(name + '\n')
