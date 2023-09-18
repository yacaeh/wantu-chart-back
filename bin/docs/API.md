
# API Documentation

## 기본사항
 - API HOST: `http://backend.wantu.io/`
 - GET Request: 요청 Parameter는 `Query string` 형식을 기본전제로 합니다.
 - POST Request: 요청 Parameter는 `Request body`에 `application/json` 형식을 기본전제로 합니다.
 - POST Request 요청시 body의 크기가 250MB를 넘을 수 없습니다.
 - `HTTP status code`로 request의 상태를 나타냅니다. (응답코드 설명 참고)

# API

## 0. image 업로드 API
### POST /api/v1/s3/upload/image

*Request*
```
headers:  {"enctype" : "multipart/form-data"}
body: form-data =>  key: file   value: 파일선택
```

*Response*

*Example(Response)*
```
{
    "url": "https://wantu-static.s3.ap-northeast-2.amazonaws.com/image/image-2021-09-14-833117.png"
}
```

## 1. 이메일 중복체크 API
### POST /api/v1/email-duplicate-check

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _email_ | `String` | 중복체크하려는 email 입니다. |

*Example(Request)*
```
{
    "email":"internet@kaist.ac.kr"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | response body의 data를 확인하세요. |
| _400_ | 잘못된 요청입니다. response body의 detail을 읽어보세요. |


## 2. 회원가입 API
### POST /api/v1/user/profile

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _email_ `(optional)` | `String` | 회원가입하려는 계정의 email 입니다. |
| _name_ | `String` | 회원가입하려는 사용자의 이름 입니다. |
| _phone_number_ | `String` | 회원가입하려는 사용자의 전화번호 입니다.|
| _password_ | `String` | 회원가입하려는 계정의 비밀번호입니다. (`password` or `sns` 둘중 하나는 필수입니다.)|
| _sns_ `(optional)` | `String` | sns 연동 회원가입인 경우 채워지는 field입니다. [`google`, `facebook`, `kakao`, `naver`]|
| _image_url_ `(optional)` | `String` | 회원가입하려는 계정의 profile image url 입니다. |
| _introduction_ `(optional)` | `String` | 회원가입하려는 계정의 소개글 입니다. |
| _hashtags_ `(optional)` | `String Array` | 새로운 해쉬태그들 입니다. |
| _facebook_ `(optional)` | `String` | 회원가입하려는 계정의 facebook SNS link 입니다. |
| _instagram_ `(optional)` | `String` | 회원가입하려는 계정의 instagram SNS link 입니다. |
| _personal_site_ `(optional)` | `String` | 회원가입하려는 계정의 블로그, 개인사이트 입니다. |


*Example(Request)*
```
{
    "name":"테스트",
    "phone_number":"010-5346-4101",
    "password":"test",
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 회원가입 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 3. 로그인 API
### POST /api/v1/user/login

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _phone_number_ | `String` | 로그인하려는 계정의 phone_number 입니다. |
| _password_ `(optional)` | `String` | 로그인하려는 계정의 비밀번호입니다. (`password` or `sns` 둘중 하나는 필수입니다.)|
| _sns_ `(optional)` | `String` | sns 연동 로그인하는 경우 채워지는 field입니다. [`google`, `facebook`, `kakao`, `naver`]|
| _keep_logged_in_ `(optional)` | `Boolean` | 로그인 유지 여부입니다. |


*Example(Request)*
```
{
    "phone_number":"01085151619",
    "password":"test"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 로그인 되었습니다. |
| _400_ | 잘못된 phone_number 또는 password 또는 sns 입니다. response body의 detail을 읽어보세요. |


## 4. 내 회원정보 받기 API
### GET /api/v1/user/profile

*Request*
```
필요한 정보가 없습니다.
```

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `User Detail Object` | 자세한 회원 정보를 담고있는 Object입니다. |

*Example(Response)*
```
{
    "data": {
        "user_id": 1,
        "hashtags": [
            "와인러버",
            "레드와인"
        ],
        "email": "internet@kaist.ac.kr",
        "name": "김동현",
        "phone_number": "010-5346-4101",
        "image_url": null,
        "introduction": "안녕 나는 김동현이라고해~",
        "facebook": null,
        "instagram": null,
        "personal_site": null
    }
}
```


## 5. 회원정보수정 API
### PUT /api/v1/user/profile

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _name_ `(optional)` | `String` | 새로운 이름 입니다. |
| _password_ `(optional)` | `String` | 새로운 비밀번호 입니다. |
| _phone_number_ `(optional)` | `String` | 새로운 핸드폰 번호 입니다. |
| _hashtags_ `(optional)` | `String Array` | 새로운 해쉬태그들 입니다. |
| _image_url_ `(optional)` | `String` | 새로운 profile image url 입니다. |
| _introduction_ `(optional)` | `String` | 새로운 소개글 입니다. |
| _facebook_ `(optional)` | `String` | 새로운 sns facebook link 입니다. |
| _instagram_ `(optional)` | `String` | 새로운 sns instagram link 입니다. |
| _personal_site_ `(optional)` | `String` | 새로운 블로그, 개인사이트 입니다. |
| _bank_ `(optional)` | `String` | 회원님의 은행 종류 입니다. |
| _bank_account_ `(optional)` | `String` | 회원님의 은행 계좌번호 입니다. |

*Example(Request)*
```
{
    "hashtags": ["와인러버", "레드와인"],
    "introduction": "안녕 나는 김동현이라고해~"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 변경되었습니다. |


## 6. 회원정보삭제 API
### DELETE /api/v1/user/int:user_id

*Request*
```
필요한 정보가 없습니다.
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 삭제 되었습니다. |
| _400_ | reponse body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. |


## 7. feed 만들기 API
### POST /api/v1/feed

*Request*

| key | type   | 설명 |
| --- | :----: | --- |
| _title_ | `String` | Cheeting의 제목 입니다. |
| _start_at_ | `String` | Cheeting의 시작 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
| _place_name_ | `String` | Cheeting의 장소 입니다.|
| _latitude_ | `Float` | Cheeting 장소의 위도 입니다.|
| _longitude_ | `Float` | Cheeting 장소의 경도 입니다.|
| _city_ | `String` | Cheeting 장소의 시/도 입니다. |
| _county_ | `String` | Cheeting 장소의 군/구 입니다. |
| _people_limit_ | `Integer` | Cheeting의 모집하려는 인원 입니다. |
| _participation_fee_ | `Integer` | Cheeting의 참가비 입니다. |
| _open_chat_link_ | `String` | Cheeting 오픈 카톡 방 링크입니다. |
| _hashtags_ | `String Array` | Cheeting 해쉬태그들 입니다. |
| _wines_ | `Wine Object Array` | Wine들 정보를 담고있는 Array 입니다. |
| _introduction_ `(optional)` | `String` | Cheeting 소개글 입니다. |
| _image_url_ `(optional)` | `String` | Cheeting 썸네일 image url 입니다. |
| _place_detail_ `(optional)` | `String` | Cheeting 장소의 자세한 내용 입니다. |


*Example(Request)*
```
{
    "title": "치팅 함께해요~",
    "start_at": "2021-10-05 20:00:00",
    "place_name": "스빌 402호",
    "latitude": 36.369157,
    "longitude": 127.355930,
    "city": "대전광역시",
    "county": "유성구",
    "people_limit": 7,
    "participation_fee": 10000,
    "open_chat_link": "https://open.kakao.com/o/gNllAwCd",
    "hashtags": ["와인러버", "함께해요"],
    "wines": [
        {
            "name": "test wine",
            "grape_variety": "포도품종",
            "vintage": 2017,
            "image_urls": []
        }
    ]
}
```

*Response*

| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 8. feed 리스트 보기 API
### GET /api/v1/feed

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Feed Summury Object Array` | 요약된 Feed 정보를 담고있는 Object의 Array 입니다. |
| _total_ | `Integer` | pagenation을 위한 전체 개수입니다. |

*Example(Response)*
```
{
  "data": [
    {
      "feed_id": 1,
      "user": {
        "user_id": 1,
        "name": "테스트",
        "image_url": null,
        "email": "kyoungin100@gmail.com",
        "introduction": "안녕 나는 김동현이라고해~"
      },
      "hashtags": [
        "hashtag1"
      ],
      "title": "영상 제목",
      "introduction": "콘텐츠 부연설명부",
      "content": "프로젝트 상세 설명",
      "financial_plan": "예산 상세 설명",
      "thumbnail_image_url": null,
      "teaser_url": "https://example.com",
      "video_url": "https://example.com",
      "image_urls": "[https://example.com]",
      "start_at": "2022-08-12T20:00:00",
      "end_at": "2022-08-12T20:00:00",
      "release_at": "2022-09-22T20:00:00",
      "goal_amount": 5000000,
      "minimum_amount": 1000,
      "maximum_amount": 5000000,
      "investment_cnt": 0,
      "investment_amount": 0,
      "total_nft": 1,
      "nft_urls": null,
      "nft_benefit": "NFT 혜택 설명",
      "created_at": "2022-09-14T15:33:17",
      "yield_amount": null,
      "updated_at": "2022-09-14T15:33:17",
      "mine": true,
      "like_cnt": 0,
      "whether_liked": false,
      "reply_cnt": 0,
      "play_cnt": 0,
      "status": "PENDING"
    }
  ],
  "total": 1
}
```


## 9. My Feed API
### GET /api/v1/feed/user/<int:user_id>
### 내가 만든 Feed 리스트

*Example(Request)*
```
/api/v1/feed/user/30
```

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Feed Detail Object` | 자세한 Feed 정보를 담고있는 Object 입니다. |
| _total_ | `Integer` | pagenation을 위한 전체 개수입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "feed_id": 1,
        "user": {
            "user_id": 1,
            "name": "테스트",
            "image_url": null,
            "email": "kyoungin100@gmail.com",
            "introduction": "안녕 나는 김동현이라고해~"
        },
        "hashtags": [
            "hashtag1"
        ],
        "title": "영상 제목",
        "introduction": "콘텐츠 부연설명부",
        "content": "프로젝트 상세 설명",
        "financial_plan": "예산 상세 설명",
        "thumbnail_image_url": null,
        "teaser_url": "https://example.com",
        "video_url": "https://example.com",
        "image_urls": "[https://example.com]",
        "start_at": "2022-08-12T20:00:00",
        "end_at": "2022-08-12T20:00:00",
        "release_at": "2022-09-22T20:00:00",
        "goal_amount": 5000000,
        "minimum_amount": 1000,
        "maximum_amount": 5000000,
        "investment_cnt": 0,
        "investment_amount": 0,
        "total_nft": 1,
        "nft_urls": null,
        "nft_benefit": "NFT 혜택 설명",
        "created_at": "2022-09-14T15:33:17",
        "yield_amount": null,
        "updated_at": "2022-09-14T15:33:17",
        "mine": true,
        "like_cnt": 0,
        "whether_liked": false,
        "reply_cnt": 0,
        "play_cnt": 0,
        "status": "PENDING"
        }
    ],
    "total": 1
}
```


## 10. Feed 자세하게 보기 API
### GET /api/v1/feed/int:feed_id

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Feed Detail Object` | 자세한 Feed 정보를 담고있는 Object 입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "feed_id": 1,
        "user": {
            "user_id": 1,
            "name": "테스트",
            "image_url": null,
            "email": "kyoungin100@gmail.com",
            "introduction": "안녕 나는 김동현이라고해~"
        },
        "hashtags": [
            "hashtag1"
        ],
        "title": "영상 제목",
        "introduction": "콘텐츠 부연설명부",
        "content": "프로젝트 상세 설명",
        "financial_plan": "예산 상세 설명",
        "thumbnail_image_url": null,
        "teaser_url": "https://example.com",
        "video_url": "https://example.com",
        "image_urls": "[https://example.com]",
        "start_at": "2022-08-12T20:00:00",
        "end_at": "2022-08-12T20:00:00",
        "release_at": "2022-09-22T20:00:00",
        "goal_amount": 5000000,
        "minimum_amount": 1000,
        "maximum_amount": 5000000,
        "investment_cnt": 0,
        "investment_amount": 0,
        "total_nft": 1,
        "nft_urls": null,
        "nft_benefit": "NFT 혜택 설명",
        "created_at": "2022-09-14T15:33:17",
        "yield_amount": null,
        "updated_at": "2022-09-14T15:33:17",
        "mine": true,
        "like_cnt": 0,
        "whether_liked": false,
        "reply_cnt": 0,
        "play_cnt": 0,
        "status": "PENDING"
        }
    ],
}
```


## 11. feed 글 리스트 Search API
### GET /api/v1/feed?search=배기&

*Example(Request)*
```
/api/v1/feed?search=배기&
```

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Feed Object Array` | Feed 글 정보를 담고있는 Object의 Array 입니다. |
| _total_ | `Integer` | pagenation을 위한 전체 개수입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "feed_id": 1,
        "user": {
            "user_id": 1,
            "name": "테스트",
            "image_url": null,
            "email": "kyoungin100@gmail.com",
            "introduction": "안녕 나는 김동현이라고해~"
        },
        "hashtags": [
            "hashtag1"
        ],
        "title": "영상 제목",
        "introduction": "콘텐츠 부연설명부",
        "content": "프로젝트 상세 설명",
        "financial_plan": "예산 상세 설명",
        "thumbnail_image_url": null,
        "teaser_url": "https://example.com",
        "video_url": "https://example.com",
        "image_urls": "[https://example.com]",
        "start_at": "2022-08-12T20:00:00",
        "end_at": "2022-08-12T20:00:00",
        "release_at": "2022-09-22T20:00:00",
        "goal_amount": 5000000,
        "minimum_amount": 1000,
        "maximum_amount": 5000000,
        "investment_cnt": 0,
        "investment_amount": 0,
        "total_nft": 1,
        "nft_urls": null,
        "nft_benefit": "NFT 혜택 설명",
        "created_at": "2022-09-14T15:33:17",
        "yield_amount": null,
        "updated_at": "2022-09-14T15:33:17",
        "mine": true,
        "like_cnt": 0,
        "whether_liked": false,
        "reply_cnt": 0,
        "play_cnt": 0,
        "status": "PENDING"
        }
    ],
    "total": 1
}
```


## 12. feed 글 수정 API
### PUT /api/v1/feed/int:feed_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _hashtag_ | `String Array` | 해시태그들 입니다. |
| _content_ | `String` | 상세 설명 입니다. |
| _thumbnail_image_url_ | `String` | thumbnail_url 입니다. |
| _teaser_url_ | `String` | teaser_url 입니다. |
| _video_url_ | `String` | video_url 입니다. |
| _title_ | `String` | 제목 입니다. |
| _image_urls_ | `String Array` | image_urls 입니다. |
| _introduction_ | `String` | 부연설명부 입니다. |
| _schedule_ | `String` | 제작 및 업로드 일정 설명 입니다. |
| _financial_plan_ | `String` | 예산 상세 설명 입니다. |
| _start_at_ | `String` | 시작 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
| _end_at_ | `String` | 종료 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
| _release_at_ | `String` | release 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
| _status_ | `String` | 상태 입니다.|
| _goal_amount_ | `Integer` | goal_amount 입니다.|
| _minimum_amount_ | `Integer` | minimum_amount 입니다.|
| _maximum_amount_ | `Integer` | maximum_amount 입니다.|
| _total_nft_ | `Integer` | total_nft 입니다.|
| _nft_benefit_ | `String` | NFT 혜택 설명 입니다.|
| _nft_urls_ | `String Array` | nft_urls 입니다.|
| _yield_amount_ | `Float` | yield_amount 입니다.|
| _contract_address_ | `String` | contract_address 입니다.|


*Example(Request)*
```
{
    "hashtags": [
        "힙합",
        "창모"
    ],
    "content":"업데이트된 콘텐츠"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 수정 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. 자신이 만든 게시글이 아닙니다. |


## 13. feed 글 삭제 API
### DELETE /api/v1/feed/int:feed_id

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 삭제 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. 자신이 만든 게시글이 아닙니다. |


## 14. 댓글 리스트 보기 API
### GET /api/v1/common/reply

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _feed_id_ | `Integer` | 댓글리스트를 보고싶은 Feed id를 입력합니다. |

*Example(Request)*
```
/api/v1/common/reply?feed_id=1
```

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Reply Object Array` | Reply 정보를 담고있는 Object의 Array 입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "reply_id": 6,
        "user": {
            "user_id": 10,
            "name": "nucp3",
            "image_url": null,
            "introduction": null
        },
        "text": "reply1",
        "created_at": "2022-09-15T11:22:27",
        "updated_at": "2022-09-15T11:22:27",
        "nested_reply_cnt": 0,
        "like_cnt": 0,
        "whether_liked": false
        },
        {
        "reply_id": 5,
        "user": {
            "user_id": 9,
            "name": "kyoungin",
            "image_url": null,
            "introduction": null
        },
        "text": "reply1",
        "created_at": "2022-09-15T11:21:04",
        "updated_at": "2022-09-15T11:21:04",
        "nested_reply_cnt": 0,
        "like_cnt": 0,
        "whether_liked": false
        },
        {
        "reply_id": 4,
        "user": {
            "user_id": 9,
            "name": "kyoungin",
            "image_url": null,
            "introduction": null
        },
        "text": "reply1",
        "created_at": "2022-09-15T11:19:48",
        "updated_at": "2022-09-15T11:19:48",
        "nested_reply_cnt": 0,
        "like_cnt": 0,
        "whether_liked": false
        }
    ]
}
```

## 15. 댓글 추가 API
### POST /api/v1/common/reply

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _feed_id_ | `Integer` | 댓글 달고싶은 Feed id를 입력합니다. |
| _text_ | `String` | 추가하려는 댓글 입니다. |

*Example(Request)*
```
{
    "feed_id": 1,
    "text": "reply1"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 16. 댓글 수정 API
### PUT /api/v1/common/reply/int:reply_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _text_ | `String` | 수정된 문구 입니다. |

*Example(Request)*
```
{
	"text": "edit reply"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 수정 되었습니다. |


## 17. 댓글 삭제 API
### DELETE /api/v1/common/reply/int:reply_id

*Request*
```
필요한 정보가 없습니다.
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 삭제 되었습니다. |


## 18. 대댓글 리스트 보기 API
### GET /api/v1/common/reply/int:reply_id/nested_reply

*Example(Request)*
```
/api/v1/common/reply/5/nested_reply
```

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Nested Reply Object Array` | Nested Reply 정보를 담고있는 Object의 Array 입니다. |
| _total_ | `Integer` | pagenation을 위한 전체 개수입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "nested_reply_id": 3,
        "user": {
            "user_id": 9,
            "name": "kyoungin",
            "image_url": null,
            "introduction": null
        },
        "text": "nested reply1",
        "created_at": "2022-09-19T10:54:30",
        "updated_at": "2022-09-19T10:54:30",
        "like_cnt": 0,
        "whether_liked": false
        }
    ]
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 19. 대댓글 추가 API
### POST /api/v1/common/reply/int:reply_id/nested_reply

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _text_ | `String` | 추가하려는 대댓글 입니다. |

*Example(Request)*
```
{
    "text": "nested reply1"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 20. 대댓글 수정 API
### PUT /api/v1/common/reply/int:reply_id/nested_reply/int:nested_reply_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _text_ | `String` | 수정된 문구 입니다. |

*Example(Request)*
```
{
	"text": "edit nested reply"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 수정 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 21. 대댓글 삭제 API
### DELETE /api/v1/common/reply/int:reply_id/nested_reply/int:nested_reply_id

*Request*
```
필요한 정보가 없습니다.
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 삭제되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 22. 좋아요 등록/취소 API
### POST /api/v1/common/like

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _feed_id_ `(optional)` | `Integer` | 좋아요(등록/취소)하려는 feed의 id 입니다. |
| _community_id_ `(optional)` | `Integer` | 좋아요(등록/취소)하려는 community의 id 입니다. |
| _reply_id_ `(optional)` | `Integer` | 좋아요(등록/취소)하려는 댓글의 id 입니다. |
| _nested_reply_id_ `(optional)` | `Integer` | 좋아요(등록/취소)하려는 대댓글의 id 입니다. |

*Example(Request)*
```
{
	"reply_id": 3
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 (좋아요 등록/ 좋아요 취소) 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 23. 좋아요 가져오기 API
### GET /api/v1/common/like

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": [
        {
        "like_id": 4,
        "user": 9,
        "feed": null,
        "reply": 4,
        "nested_reply": null
        }
    ],
    "total": 1
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 24. 팔로우 등록/취소 API
### POST /api/v1/following/user/int:user_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _follow_user_id_ `(optional)` | `Integer` | 팔로우(등록/취소)하려는 유저의 id 입니다. |
| _hashtag_id_ `(optional)` | `Integer` | 팔로우(등록/취소)하려는 해시태그의 id 입니다. |

*Example(Request)*
```
{
	"follow_user_id": 4
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 (팔로우 등록/ 팔로우 취소) 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 25. 팔로워 정보 API
### GET /api/v1/follower/user/int:user_id

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": [
        {
        "user_id": 9,
        "name": "kyoungin",
        "image_url": null,
        "email": "kyoungin100@gmail.com",
        "introduction": null,
        "whether_following": false
        }
    ],
    "total": 1
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 26. 팔로잉 정보 API
### GET /api/v1/following/user/int:user_id

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": [
        {
        "user_id": 10,
        "name": "nucp3",
        "image_url": null,
        "email": "nucp3@naver.com",
        "introduction": null,
        "whether_following": false
        }
    ],
    "total": 1
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 27. 재생 카운트 추가 API
### POST /api/v1/common/play

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _feed_id_ | `Integer` | 재생 카운트를 추가하려는 feed의 id 입니다. |

*Example(Request)*
```
{
	"feed_id": 4
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 추가 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 28. 재생 카운트 조회 API
### GET /api/v1/common/play/feed/int:feed_id

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": [
        {
        "user_id": 10,
        "name": "nucp3",
        "image_url": null,
        "email": "nucp3@naver.com",
        "introduction": null,
        "whether_following": false
        }
    ],
    "total": 1
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 추가 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 29. 피드 투자 조회 API
### GET /api/v1/feed/int:feed_id/investment

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": {
        "feed_id": 2,
        "user": {
        "user_id": 9,
        "name": "kyoungin",
        "image_url": null,
        "email": "kyoungin100@gmail.com",
        "introduction": null
        },
        "mine": false,
        "investment_cnt": 1,
        "investment_amount": 4000,
        "whether_invested": false
    }
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 30. 피드 투자 API
### POST /api/v1/common/investment/int:feed_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _amount_ | `Integer` | 투자하려는 금액입니다. |

*Example(Request)*
```
{
    "amount": 4000,
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 투자 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 31. 피드 투자 철회 API
### DELETE /api/v1/common/investment/int:feed_id

*Request*
```
필요한 정보가 없습니다.
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 삭제 되었습니다. |


## 32. 예치금 입출금 API
### POST /api/v1/common/deposit

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _type_ | `String` | 입금, 출금 구분입니다. |
| _amount_ | `Integer` | 입출금하려는 금액입니다. |

*Example(Request)*
```
{
    "type": "DEPOSIT",
    "amount": 4000
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 33. 예치금 상태변경 API
### PUT /api/v1/common/deposit/int:deposit_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _status_ | `String` | 예치금 상태 입니다. |

*Example(Request)*
```
{
    "status": "CONFIRM"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 수정 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 34. 예치금 조회 API
### GET /api/v1/common/deposit/int:feed_id

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": [
        {
        "deposit_id": 14,
        "type": "DEPOSIT",
        "amount": 5000,
        "status": "PENDING",
        "created_at": "2022-09-26T10:32:28",
        "updated_at": "2022-09-26T10:32:28",
        "user": 12
        },
        {
        "deposit_id": 13,
        "type": "DEPOSIT",
        "amount": 1000,
        "status": "PENDING",
        "created_at": "2022-09-26T10:32:18",
        "updated_at": "2022-09-26T10:32:18",
        "user": 12
        }
    ]
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 35. feed 상태 수정 API
### PUT /api/v1/feed/int:feed_id/status

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _status_ | `String` |  feed 상태 입니다. |

*Status 상태 정리*
| status | 설명 |
| --- | :----: | --- |
| _PENDING_ |  임시저장 상태 or 프로젝트가 생성되기 전 |
| _OPEN_ |  프로젝트 생성 이후 or 프로젝트 마감 기한 전 |
| _SUCCESS_ |  프로젝트 금액 목표 이상 and (프로젝트 마감 or 크리에이터가 목표 달성 버튼 클릭 시) |
| _FAILED_ |  프로젝트 금액 목표 미만 and (프로젝트 마감 or 크리에이터가 목표 달성 버튼 클릭 시) |
| _CANCELED_ |  프로젝트 취소(COMPLETE인 경우 취소 불가능. PENDING에서는 CANCELED가 아닌 삭제만 가능) |
| _COMPLETE_ |  본 영상이 올라온 경우(SUCCESS, FAILED인 경우에만 가능) |

*Example(Request)*
```
{
    "status": "SUCCESS"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 수정 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _203_ | 권한이 없습니다. |


## 36. feed 메인 화면 topviews 조회 API
### GET /api/v1/feed/main/topviews

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": [
        {
        "deposit_id": 14,
        "type": "DEPOSIT",
        "amount": 5000,
        "status": "PENDING",
        "created_at": "2022-09-26T10:32:28",
        "updated_at": "2022-09-26T10:32:28",
        "user": 12
        },
        {
        "deposit_id": 13,
        "type": "DEPOSIT",
        "amount": 1000,
        "status": "PENDING",
        "created_at": "2022-09-26T10:32:18",
        "updated_at": "2022-09-26T10:32:18",
        "user": 12
        }
    ]
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 37. feed 메인 화면 recommendations 조회 API
### GET /api/v1/feed/main/recommendations

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": [
        {
        "deposit_id": 14,
        "type": "DEPOSIT",
        "amount": 5000,
        "status": "PENDING",
        "created_at": "2022-09-26T10:32:28",
        "updated_at": "2022-09-26T10:32:28",
        "user": 12
        },
        {
        "deposit_id": 13,
        "type": "DEPOSIT",
        "amount": 1000,
        "status": "PENDING",
        "created_at": "2022-09-26T10:32:18",
        "updated_at": "2022-09-26T10:32:18",
        "user": 12
        }
    ]
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 38. feed 메인 화면 topinvestments 조회 API
### GET /api/v1/feed/main/topinvestments

*Request*
```
필요한 정보가 없습니다.
```

*Example(Response)*
```
{
    "data": [
        {
        "deposit_id": 14,
        "type": "DEPOSIT",
        "amount": 5000,
        "status": "PENDING",
        "created_at": "2022-09-26T10:32:28",
        "updated_at": "2022-09-26T10:32:28",
        "user": 12
        },
        {
        "deposit_id": 13,
        "type": "DEPOSIT",
        "amount": 1000,
        "status": "PENDING",
        "created_at": "2022-09-26T10:32:18",
        "updated_at": "2022-09-26T10:32:18",
        "user": 12
        }
    ]
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 39. 피드별 episode 조회 API
### GET /api/v1/common/episode/feed/int:feed_id

**Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Episode Summury Object Array` | 요약된 Episode 정보를 담고있는 Object의 Array 입니다. |

*Example(Response)*
```
{
    "data": {
        "episode_id": 1,
        "title": "에피소드 제목2",
        "url": "https://example.com2",
        "thumbnail_image_url": "https://example.com2",
        "subtitle": "에피소드 부제목2",
        "content": "에피소드 상세 설명2",
        "release_at": "2022-12-19T11:38:35.646977",
        "created_at": "2022-12-19T11:38:35.646977",
        "updated_at": "2022-12-19T16:21:43.072391",
        "user": 4,
        "feed": 3
    }
}
```


## 40. episode 만들기 API
### POST /api/v1/common/episode/feed/int:feed_id

*Request*
```
| key | type   | 설명 |
| --- | :----: | --- |
| _title_ | `String` | 에피소드 제목 입니다. |
| _url_ | `String` | url 입니다. |
| _thumbnail_image_url_ | `String` | 썸네일 url 입니다. |
| _subtitle_ | `String` | 에피소드 부제목 입니다. |
| _content_ | `String` | 에피소드 상세 설명 입니다. |
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. 본인의 feed가 아닙니다. |


## 41. episode 조회 API
### GET /api/v1/common/episode/int:episode_id

**Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Episode Summury Object Array` | 요약된 Episode 정보를 담고있는 Object의 Array 입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "episode_id": 1,
        "user": {
            "user_id": 4,
            "name": "kyoungin100",
            "image_url": null,
            "introduction": null
        },
        "feed": {
            "feed_id": 3,
            "content": "프로젝트 상세 설명",
            "thumbnail_image_url": "https://cdn.wantu.io/video/thumb-2022-12-15-322438.jpg",
            "teaser_url": "https://img.youtube.com/vi/rIfJrhfJadk/0.jpg",
            "created_at": "2022-11-29T01:51:47.502029",
            "updated_at": "2022-11-29T01:51:47.502054",
            "title": "갸르포차!",
            "image_urls": "['https://img.youtube.com/vi/rIfJrhfJadk/0.jpg', 'https://img.youtube.com/vi/rIfJrhfJadk/0.jpg']",
            "introduction": "콘텐츠 부연설명부",
            "schedule": "영상 제작 및 업로드 일정 설명",
            "financial_plan": "예산 상세 설명",
            "start_at": "2022-08-12T20:00:00",
            "end_at": "2022-08-30T20:00:00",
            "release_at": "2022-09-22T20:00:00",
            "status": "PENDING",
            "goal_amount": 5000000,
            "minimum_amount": 1000,
            "maximum_amount": 5000000,
            "total_nft": 1,
            "nft_benefit": "NFT 혜택 설명",
            "nft_urls": null,
            "investment_amount": 0,
            "yield_amount": null,
            "contract_address": null,
            "user": 4,
            "hashtag": [
            3,
            4
            ]
        }
        }
    ]
}
```


## 42. episode 수정 API
### PUT /api/v1/common/episode/int:episode_id

*Request*
```
| key | type   | 설명 |
| --- | :----: | --- |
| _title_ | `String` | 에피소드 제목 입니다. |
| _url_ | `String` | url 입니다. |
| _thumbnail_image_url_ | `String` | 썸네일 url 입니다. |
| _subtitle_ | `String` | 에피소드 부제목 입니다. |
| _content_ | `String` | 에피소드 상세 설명 입니다. |
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. 본인의 feed가 아닙니다. |


## 43. episode 삭제 API
### DELETE /api/v1/common/episode/int:episode_id

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 삭제 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. 자신이 만든 게시글이 아닙니다. |


## 44. event 가져오기 API
### GET /api/v1/common/event

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Event Summury Object Array` | 요약된 Event 정보를 담고있는 Object의 Array 입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "event_id": 1,
        "type": "SIGNUP",
        "name": "회원가입 선착순",
        "status": "PENDING",
        "point": 1000,
        "number": 1000,
        "start_at": "2022-08-12T20:00:00",
        "end_at": "2022-08-30T20:00:00",
        "created_at": "2023-01-05T15:27:31.632319",
        "updated_at": "2023-01-05T15:27:31.632319"
        }
    ]
}
```


## 45. event 생성 API
### POST /api/v1/common/event

*Request*
```
| key | type   | 설명 |
| --- | :----: | --- |
| _type_ | `String` | event 구분 입니다. |
| _name_ | `String` | event 명칭 입니다. |
| _point_ | `Integer` | 몇 포인트를 제공할 지 구분 입니다. |
| _number_ | `Integer` | 몇 명에게 제공할 지 구분 입니다. |
| _start_at_ | `String` | 포인트 시작 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
| _end_at_ | `String` | 포인트 종료 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
```

*Example(Request)*
```
{
    "type": "signup",
    "name": "회원가입 선착순",
    "point": 1000,
    "number": 1000,
    "start_at": "2022-08-12T20:00:00",
    "end_at": "2022-08-30T20:00:00",
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. |


## 46. event 상세 API
### GET /api/v1/common/event/int:event_id

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Event Summury Object Array` | 요약된 Event 정보를 담고있는 Object의 Array 입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "event_id": 1,
        "type": "signup",
        "name": "회원가입 선착순",
        "status": "PENDING",
        "point": 1000,
        "number": 1000,
        "start_at": "2022-08-12T20:00:00",
        "end_at": "2022-08-30T20:00:00",
        "created_at": "2023-01-05T15:27:31.632319",
        "updated_at": "2023-01-05T15:27:31.632319"
        }
    ]
}
```


## 47. event 수정 API
### PUT /api/v1/common/event/int:episode_id

*Request*
```
| key | type   | 설명 |
| --- | :----: | --- |
| _type_ | `String` | event 구분 입니다. |
| _name_ | `String` | event 명칭 입니다. |
| _status_ | `String` | PENDING, CONFIRMED 구분 입니다. |
| _point_ | `Integer` | 몇 포인트를 제공할 지 구분 입니다. |
| _number_ | `Integer` | 몇 명에게 제공할 지 구분 입니다. |
| _start_at_ | `String` | 포인트 시작 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
| _end_at_ | `String` | 포인트 종료 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
```

*Example(Request)*
```
{
    "type": "signup",
    "name": "회원가입 선착순",
    "status": "CONFIRMED",
    "point": 1000,
    "number": 1000,
    "start_at": "2022-08-12T20:00:00",
    "end_at": "2022-08-30T20:00:00",
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 수정 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. |


## 48. 유저 point 리스트 가져오기 API
### GET /api/v1/common/point/int:user_id

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Point Summury Object Array` | 요약된 Point 정보를 담고있는 Object의 Array 입니다. |

*Example(Response)*
```
{
    "data": {
        "point_id": 1,
        "point": 1000,
        "type": "EVENT",
        "type_id": "1",
        "status": "EARNED",
        "start_at": "2022-08-12T20:00:00",
        "end_at": "2022-08-30T20:00:00",
        "created_at": "2023-01-05T15:58:19.423631",
        "updated_at": "2023-01-05T15:58:19.423631",
        "user": 4
    }
}
```


## 49. 유저 point 부여 API
### POST /api/v1/common/point/int:user_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _point_ | `Integer` | 부여 point 입니다. |
| _type_ | `String` | 이벤트로 쌓인 포인트인지, 영상 시청으로 쌓인 포인트인지 구분 입니다. |
| _type_id_ | `String` | 이벤트면 event_id, 레퍼럴이면 feed_id 혹은 episode_id 입니다. |
| _status_ | `String` | 적립인지, 사용인지 구분 입니다. |
| _start_at_ | `String` | 포인트 시작 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |
| _end_at_ | `String` | 포인트 종료 날짜와 시간 입니다. `yyyy-mm-dd hh:mm:ss` 형식입니다. |

*Example(Request)*
```
{
    "point": 1000,
    "type": "EVENT",
    "type_id": "1",
    "status": "EARNED",
    "start_at": "2022-08-12T20:00:00",
    "end_at": "2022-08-30T20:00:00",
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. |


## 50. 커뮤니티 리스트 보기 API
### GET /api/v1/common/community

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _feed_id_ | `Integer` | 댓글리스트를 보고싶은 Feed id를 입력합니다. |

*Example(Request)*
```
/api/v1/common/community?feed_id=1
```

*Response*
| key | type  | 설명 |
| --- | :---: | --- |
| _data_ | `Community Object Array` | Community 정보를 담고있는 Object의 Array 입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "community_id": 1,
        "user": {
            "user_id": 6,
            "name": "01085151619",
            "image_url": null,
            "introduction": null
        },
        "text": "community1",
        "created_at": "2023-03-01T17:14:11.690065",
        "updated_at": "2023-03-01T17:14:11.690065",
        "reply_cnt": 0,
        "like_cnt": 0,
        "whether_liked": false,
        "label": "visitors"
        }
    ]
}
```

## 51. 커뮤니티 글 추가 API
### POST /api/v1/common/community

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _feed_id_ | `Integer` | 댓글 달고싶은 Feed id를 입력합니다. |
| _text_ | `String` | 추가하려는 댓글 입니다. |

*Example(Request)*
```
{
    "feed_id": 1,
    "text": "community1"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |
| _403_ | 권한이 없습니다. 자신이 만든 피드가 아닙니다. |


## 52. 커뮤니티 글 수정 API
### PUT /api/v1/common/community/int:community_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _text_ | `String` | 수정된 문구 입니다. |

*Example(Request)*
```
{
	"text": "edit community"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 수정 되었습니다. |
| _403_ | 권한이 없습니다. 자신이 만든 커뮤니티 글이 아닙니다. |


## 53. 커뮤니티 글 삭제 API
### DELETE /api/v1/common/community/int:community_id

*Request*
```
필요한 정보가 없습니다.
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 삭제 되었습니다. |
| _403_ | 권한이 없습니다. 자신이 만든 커뮤니티 글이 아닙니다. |


## 54. 커뮤니티 댓글 리스트 보기 API
### GET /api/v1/common/community/int:community_id/reply

*Example(Request)*
```
/api/v1/common/community/5/reply
```

*Response*
| key | type  | 설명 |
| --- | :---: | --- |2r3
| _data_ | `Reply Object Array` | Reply 정보를 담고있는 Object의 Array 입니다. |
| _total_ | `Integer` | pagenation을 위한 전체 개수입니다. |

*Example(Response)*
```
{
    "data": [
        {
        "reply_id": 2,
        "user": {
            "user_id": 6,
            "name": "01085151619",
            "image_url": null,
            "introduction": null
        },
        "text": "community reply2",
        "created_at": "2023-03-01T17:41:54.013874",
        "updated_at": "2023-03-01T17:41:54.013874",
        "nested_reply_cnt": 0,
        "like_cnt": 0,
        "whether_liked": false,
        "label": "visitors"
        },
        {
        "reply_id": 1,
        "user": {
            "user_id": 6,
            "name": "01085151619",
            "image_url": null,
            "introduction": null
        },
        "text": "community reply1",
        "created_at": "2023-03-01T17:33:08.985020",
        "updated_at": "2023-03-01T17:33:08.985020",
        "nested_reply_cnt": 0,
        "like_cnt": 0,
        "whether_liked": false,
        "label": "visitors"
        }
    ]
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _200_ | 성공적으로 조회 되었습니다. |


## 55. 커뮤니티 댓글 추가 API
### POST /api/v1/common/community/int:community_id/reply

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _text_ | `String` | 추가하려는 대댓글 입니다. |

*Example(Request)*
```
{
    "text": "community reply1"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 56. 커뮤니티 댓글 수정 API
### PUT /api/v1/common/community/int:community_id/reply/int:reply_id

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _text_ | `String` | 수정된 문구 입니다. |

*Example(Request)*
```
{
	"text": "edit community reply"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 수정 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 57. 커뮤니티 댓글 삭제 API
### DELETE /api/v1/common/community/int:community_id/reply/int:reply_id

*Request*
```
필요한 정보가 없습니다.
```

*Response*
| http status code | 설명 |
| --- | --- |
| _202_ | 성공적으로 삭제되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |


## 58. Report 생성 API
### POST /api/v1/common/report

*Request*
| key | type   | 설명 |
| --- | :----: | --- |
| _feed_id_ `(optional)` | `Integer` | 신고하려는 feed의 id 입니다. |
| _episode_id_ `(optional)` | `Integer` | 신고하려는 episode의 id 입니다. |
| _community_id_ `(optional)` | `Integer` | 신고하려는 community의 id 입니다. |
| _reply_id_ `(optional)` | `Integer` | 신고하려는 reply의 id 입니다. |
| _nested_reply_id_ `(optional)` | `Integer` | 신고하려는 nested_reply의 id 입니다. |

*Example(Request)*
```
{
    "feed_id": 1,
    "reason": "폭력적 또는 혐오스러운 콘텐츠"
}
```

*Response*
| http status code | 설명 |
| --- | --- |
| _201_ | 성공적으로 생성 되었습니다. |
| _400_ | response body의 detail을 읽어보세요. |