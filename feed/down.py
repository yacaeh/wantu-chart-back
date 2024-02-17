import requests
from bs4 import BeautifulSoup

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a') if 'kakaocdn' in a.get('href', '')]
    return links

def save_links_to_file(links, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for link in links:
            if link:  # 이제 모든 링크는 'kakaocdn'을 포함하므로 이 조건은 항상 참입니다.
                file.write(link + '\n')

url = 'https://fpwjemkiyomi.tistory.com/132'
links = get_links(url)
save_links_to_file(links, 'links.txt')
print(f"Links have been saved to 'links.txt'")