import app.models as models
from rest_framework import serializers
from drf_yasg import openapi
from django.db.models import Avg, Count, Min, Sum


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hashtag
        fields = '__all__'


class FeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feed
        fields = '__all__'


class FeedHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeedHashtag
        fields = '__all__'


class UserSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'name', 'image_url', 'email', 'introduction')


class FeedSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    hashtags = serializers.SerializerMethodField(method_name='_hashtags', read_only=True)
    mine = serializers.SerializerMethodField('_is_mine')
    like_cnt = serializers.SerializerMethodField('_like_cnt')
    whether_liked = serializers.SerializerMethodField('_whether_liked')
    reply_cnt = serializers.SerializerMethodField('_reply_cnt')

    def _hashtags(self, obj):
        hashtags = list(models.FeedHashtag.objects.filter(feed=obj.feed_id).values_list('hashtag__text', flat=True))
        return hashtags

    def _is_mine(self, obj):
        user_id = self.context.get('user_id')
        return obj.user_id == user_id

    def _like_cnt(self, obj):
        return obj.like_set.count()

    def _whether_liked(self, obj):
        user_id = self.context.get('user_id')
        return bool(obj.like_set.filter(user_id=user_id, feed_id=obj.feed_id))

    def _reply_cnt(self, obj):
        return obj.reply_set.count()


    class Meta:
        model = models.Feed
        fields = ('feed_id', 'user', 'hashtags', 'title', 'content', 'image_urls','created_at', 'updated_at', 'mine', 'like_cnt', 'whether_liked', 'reply_cnt')


class FeedMainSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feed
        fields = '__all__'
