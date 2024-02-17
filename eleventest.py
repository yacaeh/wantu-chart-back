import requests

url = "https://api.elevenlabs.io/v1/voices"

headers = {"xi-api-key": "3cd48b77be5e9648441da9d0a9d9daea"}

response = requests.request("GET", url, headers=headers)

# 응답이 성공적인지 확인
if response.status_code == 200:
    # JSON 데이터 로드
    data = response.json()
    
    # 필요한 데이터 추출
    cloned_voices = [
        {"voice_id": voice["voice_id"], "name": voice["name"]}
        for voice in data.get("voices", [])
        if voice["category"] == "cloned"  # 'cloned' 카테고리의 목소리만 필터링
    ]
    
    print(cloned_voices)
else:
    print("API 호출 실패:", response.status_code)

clone_voices = [
  {"voice_id": "4dTMHxtCZ7AmGvfT0qNS", "name": "흑자"},
  {"voice_id": "Ax56J5BB884TXo3hhAHN", "name": "침튜부"},
  {"voice_id": "I7QkOe1ePfqu4VLOD4BS", "name": "홍구"},
  {"voice_id": "hAitD6DSq2tLQcIBUSME", "name": "김계란"},
  {"voice_id": "iKYhRmuZrJdL8pt8jI0b", "name": "크리스"},
  {"voice_id": "lN5LoEopX2q41w7Mc7gX", "name": "진용진"},
  {"voice_id": "sFRHPub0B2QMN2eooNaR", "name": "랄랄"},
  {"voice_id": "wG26p4DxynnQCOBZKMaY", "name": "나선욱"},
  {"voice_id": "xktdZI6sXB4s1ifyGZAz", "name": "슈카"},
  {"voice_id": "zEt5ObgwibbeIz86fOyJ", "name": "뻑가"}
]

import requests

CHUNK_SIZE = 1024
voice_id ='I7QkOe1ePfqu4VLOD4BS'
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "3cd48b77be5e9648441da9d0a9d9daea"
}

data = {
  "text": "이상 원투차트였습니다 수고하세요~",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75,
  }
}

response = requests.post(url, json=data, headers=headers)
with open('홍구테스트.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
