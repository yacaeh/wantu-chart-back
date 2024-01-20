import json
import re
import bcrypt, jwt
from json.decoder           import JSONDecodeError

from django.http            import JsonResponse
from django.views           import View
from django.http.response   import HttpResponse, JsonResponse

from users.utils            import login_decorator, get_user_by_request
import users.models as models
from django.db.models import Sum
from django.db.models.functions import Coalesce
import json
import app.serializers as serializers
from rest_framework.views import APIView
from rest_framework import status
from app.utils.utils import get_body, jsonify


class ReplyView(APIView):
    def get(self, request):
        rating_id = request.GET.get('rating_id', None)
        rating_id = int(rating_id) if rating_id is not None else rating_id
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        if not any([rating_id]):
            return jsonify(
                error="rating_id is required",
                status=status.HTTP_400_BAD_REQUEST
            )

        replies = models.Reply.objects.filter(
            feed=rating_id
        ).order_by('-created_at')
        replies = replies[offset:offset + limit]

        return jsonify(
            data=serializers.ReplySerializer(replies, context={'rating_id': rating_id}, many=True).data,
            status=status.HTTP_200_OK
        )

    @login_decorator
    def post(self, request):
        data = get_body(request)
        rating_id = data.get('rating_id', None)
        text = data.get('text', None)
        owner = models.User.objects.get(
                    user_id__in=models.Feed.objects.filter(
                        rating_id=rating_id).values_list('user', flat=True))

        if not any([ rating_id]):
            return jsonify(
                error="rating_id is required",
                status=status.HTTP_400_BAD_REQUEST
            )
        if text is None:
            return jsonify(
                error="text is required",
                status=status.HTTP_400_BAD_REQUEST
            )

        reply = serializers.ReplyCreateSerializer(data={
            'feed': rating_id,
            'text': text,
            'user': get_user_by_request(request).user_id
        })

        if reply.is_valid():
            reply.save()
        else:
            return jsonify(
                error=reply.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return jsonify(
            data=reply.instance.reply_id,
            status=status.HTTP_201_CREATED
        )


class ReplyDetailView(APIView):
    @login_decorator
    def put(self, request, reply_id):
        data = get_body(request)
        user_id = get_user_by_request(request).user_id
        text = data.get('text', None)

        try:
            reply = models.Reply.objects.get(reply_id=reply_id, user_id=user_id)
            reply.text = text
            reply.save()

            return HttpResponse(status=status.HTTP_202_ACCEPTED)

        except models.Reply.DoesNotExist:
            return jsonify(
                error='invalid reply_id',
                status=status.HTTP_400_BAD_REQUEST
            )

    @login_decorator

    def delete(self, request, reply_id):
        user_id = get_user_by_request(request).user_id
        try:
            reply = models.Reply.objects.get(reply_id=reply_id, user_id=user_id)
            reply.delete()
            return HttpResponse(status=status.HTTP_202_ACCEPTED)

        except models.Reply.DoesNotExist:
            return jsonify(
                error='invalid reply_id',
                status=status.HTTP_400_BAD_REQUEST
            )


class NestedReplyView(APIView):
    def get(self, request, reply_id):
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        nested_replies = models.NestedReply.objects.filter(
            reply=reply_id
        ).order_by('-created_at')
        nested_replies = nested_replies[offset:offset + limit]


        return jsonify(
            data=serializers.NestedReplySerializer(nested_replies, many=True).data,
            status=status.HTTP_200_OK
        )

    @login_decorator
    def post(self, request, reply_id):
        data = get_body(request)
        text = data.get('text', None)
        if text is None:
            return jsonify(
                error="text is required",
                status=status.HTTP_400_BAD_REQUEST
            )
        owner = models.User.objects.get(
                    user_id__in=models.Reply.objects.filter(
                        reply_id=reply_id).values_list('user', flat=True))

        feed = models.Feed.objects.get(
                    rating_id__in=models.Reply.objects.filter(
                        reply_id=reply_id).values_list('feed', flat=True))

        nested_reply = serializers.NestedReplyCreateSerializer(data={
            'text': text,
            'reply': reply_id,
            'user': get_user_by_request(request).user_id
        })

        if nested_reply.is_valid():
            nested_reply.save()
        else:
            return jsonify(
                error=nested_reply.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return jsonify(
            data=nested_reply.instance.nested_reply_id,
            status=status.HTTP_201_CREATED
        )


class NestedReplyDetailView(APIView):
    @login_decorator
    
    def put(self, request, reply_id, nested_reply_id):
        data = get_body(request)
        user_id = get_user_by_request(request).user_id
        text = data.get('text', None)

        try:
            nested_reply = models.NestedReply.objects.get(nested_reply_id=nested_reply_id, user_id=user_id)
            nested_reply.text = text
            nested_reply.save()

            return HttpResponse(status=status.HTTP_202_ACCEPTED)

        except models.NestedReply.DoesNotExist:
            return jsonify(
                error='invalid nested_reply_id',
                status=status.HTTP_400_BAD_REQUEST
            )

    @login_decorator

    def delete(self, request, reply_id, nested_reply_id):
        user_id = get_user_by_request(request).user_id
        try:
            nested_reply = models.NestedReply.objects.get(nested_reply_id=nested_reply_id, user_id=user_id)
            nested_reply.delete()
            return HttpResponse(status=status.HTTP_202_ACCEPTED)

        except models.NestedReply.DoesNotExist:
            return jsonify(
                error='invalid nested_reply_id',
                status=status.HTTP_400_BAD_REQUEST
            )


class LikeView(APIView):
    @login_decorator

    def get(self, request):
        user_id = get_user_by_request(request).user_id
        queryset = models.Like.objects.filter(user_id=user_id)

        total = len(queryset)
        likes = serializers.LikeCreateSerializer(queryset, many=True)
        return jsonify(
            data=likes.data,
            total=total,
            status=status.HTTP_200_OK
        )

    @login_decorator
    
    def post(self, request):
        data = get_body(request)
        user_id = get_user_by_request(request).user_id
        rating_id = data.get('rating_id', None)
        reply_id = data.get('reply_id', None)
        nested_reply_id = data.get('nested_reply_id', None)
        if not any([ rating_id, reply_id, nested_reply_id]):
            return jsonify(
                error="rating_id or reply_id or nested_reply_id is required",
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            like = models.Like.objects.get(
                user_id=user_id,
                rating_id=rating_id,
                reply_id=reply_id,
                nested_reply_id=nested_reply_id
            )
            like.delete()

        except models.Like.DoesNotExist:
            like = serializers.LikeCreateSerializer(data={
                'user': user_id,
                'rating': rating_id,
                'reply': reply_id,
                'nested_reply': nested_reply_id
            })
            if like.is_valid():
                like.save()
            else:
                return jsonify(
                    error=like.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        episode = serializers.EpisodeCreateSerializer(data=data)
        if episode.is_valid():
            episode = episode.save()
        else:
            return jsonify(
                error=episode.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return HttpResponse(status=status.HTTP_202_ACCEPTED)


class FollowingView(APIView):
    @login_decorator
    
    def post(self, request):
        data = get_body(request)
        user_id = get_user_by_request(request).user_id
        follow_user_id = data.get('follow_user_id', None)
        hashtag_id = data.get('hashtag_id', None)
        if not any([user_id, follow_user_id, hashtag_id]):
            return jsonify(
                error="follow_user_id or hashtag_id is required",
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            following = models.Following.objects.get(
                user_id=user_id,
                follow_user_id=follow_user_id,
                hashtag_id=hashtag_id,
            )
            following.delete()

        except models.Following.DoesNotExist:
            following = serializers.FollowingCreateSerializer(data={
                'user': user_id,
                'follow_user': follow_user_id,
                'hashtag': hashtag_id,
            })
            if following.is_valid():
                following.save()
            else:
                return jsonify(
                    error=following.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        return HttpResponse(status=status.HTTP_202_ACCEPTED)


class FollowerUserDetailView(APIView):
    
    def get(self, request, user_id):
        print("user_id",user_id)
        user_id = user_id
        my_id = get_user_by_request(request).user_id if get_user_by_request(request) else None
        print("my_id",my_id)
        follower = models.User.objects.filter(
                user_id__in=models.Following.objects.filter(
                follow_user_id=user_id).exclude(follow_user__isnull=True
                ).values_list('user', flat=True))
        print("follower",follower)

        follower_total = len(follower)
        follower = follower
        followers = serializers.UserSimpleFollowingSerializer(follower, context={'user_id': user_id, 'my_id':my_id}, many=True)

        return jsonify(
            data=followers.data,
            total=follower_total,
            status=status.HTTP_200_OK
        )


class FollowingUserDetailView(APIView):
    
    def get(self, request, user_id):
        user_id = user_id
        my_id = get_user_by_request(request).user_id if get_user_by_request(request) else 0
        following_user = models.User.objects.filter(
                user_id__in=models.Following.objects.filter(
                user_id=user_id).exclude(follow_user__isnull=True
                ).values_list('follow_user', flat=True))

        following_total = len(following_user)
        following_user = following_user
        following_users = serializers.UserSimpleFollowingSerializer(following_user, context={'user_id': user_id, 'my_id':my_id}, many=True)

        return jsonify(
            data=following_users.data,
            total=following_total,
            status=status.HTTP_200_OK
        )


class NoticeView(View):
    def get(self, request):
        notices = Notice.objects.all()
        notice_list = [{
            "id": notice.id,
            "title" : notice.title,
            "content" : notice.content,
            "type" : notice.type,
            "created_at" : notice.created_at,
            "updated_at" : notice.updated_at,
        } for notice in notices]

        return JsonResponse({"results" : notice_list}, status=200)
