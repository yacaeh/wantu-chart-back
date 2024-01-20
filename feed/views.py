import re
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Q
from rest_framework.views import APIView
import app.models as models
import feed.serializers as serializers
from rest_framework import status
from users.utils            import login_decorator, get_user_by_request
from app.utils.utils import get_body, jsonify
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema


class FeedView(APIView):
    @swagger_auto_schema(
        operation_summary="feed 리스트 보기",
        operation_description=
        """
            **Response**
            | key | type  | 설명 |
            | --- | :---: | --- |
            | _data_ | `Feed Summury Object Array` | 요약된 Feed 정보를 담고있는 Object의 Array 입니다. |
            | _total_ | `Integer` | pagenation을 위한 전체 개수입니다. |

            **Example(Response)**
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
                    },
                    "hashtags": [
                        "hashtag1"
                    ],
                    "title": "영상 제목",
                    "content": "프로젝트 상세 설명",

                    "created_at": "2022-09-14T15:33:17",
                    "updated_at": "2022-09-14T15:33:17",
                    "mine": true,
                    "like_cnt": 0,
                    "whether_liked": false,
                    "reply_cnt": 0,
                    }
                ],
                "total": 1
            }
            ```
        """,
        manual_parameters=[openapi.Parameter('search', openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING)],
        responses={
            200: "성공적으로 조회 되었습니다.",
        }
    )
    def get(self, request):
        user_id = get_user_by_request(request).id if get_user_by_request(request) else 0
        search = request.GET.get('search', '')
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        search = request.GET.get('search', '')

        queryset = models.Feed.objects.filter()
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) | Q(title__icontains=search) | Q(user__name__icontains=search) | Q(hashtag__text__icontains=search)
            ).distinct()

        queryset = queryset.order_by('-created_at')
        queryset = queryset[offset:offset + limit]
        total = len(queryset)
        feeds = serializers.FeedSerializer(queryset, many=True, context={'user_id': user_id})
        return jsonify(
            data=feeds.data,
            total=total,
            status=status.HTTP_200_OK
        )

    @login_decorator
    @transaction.atomic
    @swagger_auto_schema(
        operation_summary="feed 만들기",
        operation_description=
        """
            **Request**
            | key | type   | 설명 |
            | --- | :----: | --- |
            | _hashtag_ | `String Array` | 해시태그들 입니다. |
            | _content_ | `String` | 상세 설명 입니다. |
            | _title_ | `String` | 제목 입니다. |
            | _image_urls_ | `String Array` | image_urls 입니다. |
            | _status_ | `String` | 상태 입니다.|

            **Example(Request)**
            ```
            {
                "hashtags": ["hashtag1", "hashtag2"],
                "content":"프로젝트 상세 설명",
                "title": "영상 제목",
                "status": "PENDING",
            }
            ```
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'hashtags': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING, example="hashtag1")),
                'content': openapi.Schema(type=openapi.TYPE_STRING, example="프로젝트 상세 설명"),

            },
            required=['title','content']
        ),
        responses={
            201: "성공적으로 생성 되었습니다.",
            400: "response body의 detail을 읽어보세요.",
        }
    )
    def post(self, request):
        required_fields = ['title', 'content']
        data = get_body(request)
        #TODO: team_id를 받아서 넣어줘야함
        user= get_user_by_request(request).id
        for field in required_fields:
            if field not in data:
                return jsonify(
                    error=field + " is required.",
                    status=status.HTTP_400_BAD_REQUEST
                )

        data['user'] = user
        hashtags = data.pop('hashtags', [])
        # get team by team_id를
        print(data)
        feed = serializers.FeedCreateSerializer(data=data)
        if feed.is_valid():
            feed = feed.save()
            for text in hashtags:
                try:
                    hashtag = models.Hashtag.objects.get(text=text)
                except models.Hashtag.DoesNotExist:
                    serializer = serializers.HashtagSerializer(data={'text': text})
                    if serializer.is_valid():
                        hashtag = serializer.save()
                feed_hashtag = serializers.FeedHashtagSerializer(data={
                    'feed': feed.feed_id,
                    'hashtag': hashtag.hashtag_id
                })
                if feed_hashtag.is_valid():
                    feed_hashtag.save()
        else:
            return jsonify(
                error=feed.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return JsonResponse({"feed_id": feed.feed_id}, status=status.HTTP_201_CREATED)


class UserFeedView(APIView):
    @swagger_auto_schema(
        operation_summary="내가 만든 Feed 리스트",
        operation_description=
        """
            **Response**
            | key | type  | 설명 |
            | --- | :---: | --- |
            | _data_ | `Feed Summury Object Array` | 요약된 Feed 정보를 담고있는 Object의 Array 입니다. |
            | _total_ | `Integer` | pagenation을 위한 전체 개수입니다. |

            **Example(Response)**
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
        """,
        responses={
            200: "성공적으로 조회 되었습니다.",
        }
    )
    def get(self, request, user_id):
        userFeeds = models.Feed.objects.filter(user_id=user_id)
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        userFeeds = userFeeds.order_by('-created_at')
        userFeeds = userFeeds[offset:offset + limit]
        total = len(userFeeds)
        feeds = serializers.FeedSerializer(userFeeds, many=True, context={'user_id': user_id})
        return jsonify(
            data=feeds.data,
            total=total,
            status=status.HTTP_200_OK
        )


class FeedDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Feed 자세하게 보기",
        operation_description=
        """
            **Response**
            | key | type  | 설명 |
            | --- | :---: | --- |
            | _data_ | `Feed Summury Object Array` | 요약된 Feed 정보를 담고있는 Object의 Array 입니다. |

            **Example(Response)**
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
        """,
        responses={
            200: "성공적으로 조회 되었습니다.",
        }
    )
    def get(self, request, feed_id):
        user_id = get_user_by_request(request).id or 0
        feed = models.Feed.objects.get(feed_id=feed_id)
        return jsonify(
            data=serializers.FeedSerializer(feed, context={'user_id': user_id}).data,
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    @swagger_auto_schema(
        operation_summary="feed 글 수정",
        operation_description=
        """
            **Request**
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

            **Example(Request)**
            ```
            {
                "hashtags": [
                    "힙합",
                    "창모"
                ],
                "content":"업데이트된 콘텐츠"
            }
            ```
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'hashtags': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING, example="힙합")),
                'content': openapi.Schema(type=openapi.TYPE_STRING, example="업데이트된 콘텐츠"),
            },
        ),
        responses={
            202: "성공적으로 수정 되었습니다.",
            400: "response body의 detail을 읽어보세요.",
            403: "권한이 없습니다. 자신이 만든 게시글이 아닙니다.",
        }
    )
    def put(self, request, feed_id):
        data = get_body(request)
        user_id = get_user_by_request(request).id
        try:
            feed = models.Feed.objects.get(feed_id=feed_id)
        except models.Feed.DoesNotExist:
            return jsonify(
                error="invalid feed_id",
                status=status.HTTP_400_BAD_REQUEST
            )

        if feed.user_id != user_id:
            return jsonify(
                error="this feed is not yours.",
                status=status.HTTP_403_FORBIDDEN
            )

        for k, v in data.items():
            if k == "hashtags":
                continue
            setattr(feed, k, v)
        feed.save()

        models.FeedHashtag.objects.filter(feed=feed.feed_id).delete()
        for text in data.get('hashtags', []):
            try:
                hashtag = models.Hashtag.objects.get(text=text)
            except models.Hashtag.DoesNotExist:
                serializer = serializers.HashtagSerializer(data={'text': text})
                if serializer.is_valid():
                    hashtag = serializer.save()
            feed_hashtag = serializers.FeedHashtagSerializer(data={
                'feed': feed.feed_id,
                'hashtag': hashtag.hashtag_id
            })
            if feed_hashtag.is_valid():
                feed_hashtag.save()
            else:
                return jsonify(
                    error=feed_hashtag.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        return HttpResponse(status=status.HTTP_202_ACCEPTED)

    @login_decorator
    @transaction.atomic
    @swagger_auto_schema(
        operation_summary="feed 글 삭제",
        operation_description=
        """
            **Response**
            ```
            필요한 정보가 없습니다.
            ```
        """,
        responses={
            202: "성공적으로 삭제 되었습니다.",
            400: "response body의 detail을 읽어보세요.",
            403: "권한이 없습니다. 자신이 만든 게시글이 아닙니다.",
        }
    )
    def delete(self, request, feed_id):
        user_id = get_user_by_request(request).id
        try:
            feed = models.Feed.objects.get(feed_id=feed_id)
        except models.Feed.DoesNotExist:
            return jsonify(
                error="invalid feed_id",
                status=status.HTTP_400_BAD_REQUEST
            )

        if feed.user_id != user_id:
            return jsonify(
                error="this feed is not yours",
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            feed.delete()
            
        return HttpResponse(status=status.HTTP_202_ACCEPTED)