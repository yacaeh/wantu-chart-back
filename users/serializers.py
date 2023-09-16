from rest_framework import serializers
from .models import models

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id','name','image_url','introduction')

class ReplySerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    nested_reply_cnt = serializers.SerializerMethodField('_nested_reply_cnt')
    like_cnt = serializers.SerializerMethodField('_like_cnt')
    whether_liked = serializers.SerializerMethodField('_whether_liked')
    label = serializers.SerializerMethodField('_label')
    report_cnt = serializers.SerializerMethodField('_report_cnt')
    whether_reported = serializers.SerializerMethodField('_whether_reported')

    def _nested_reply_cnt(self, obj):
        return obj.nestedreply_set.count()

    def _like_cnt(self, obj):
        return obj.like_set.count()

    def _whether_liked(self, obj):
        return bool(obj.like_set.filter(user_id=obj.user_id, reply_id=obj.reply_id))

    def _label(self, obj):
        feed_id = self.context.get('feed_id')
        if obj.user_id == models.Feed.objects.get(feed_id=feed_id).user_id:
            return "creator"
        elif bool(models.Investment.objects.filter(user_id=obj.user_id, feed_id=feed_id)):
            return "investors"
        else:
            return "visitors"

    def _report_cnt(self, obj):
        return obj.report_set.count()

    def _whether_reported(self, obj):
        return bool(obj.report_set.filter(user_id=obj.user_id, reply_id=obj.reply_id))

    class Meta:
        model = models.Reply
        fields = ('reply_id','user','text','created_at','updated_at','nested_reply_cnt','like_cnt','whether_liked','label','report_cnt','whether_reported')



class UserSimpleFollowingSerializer(serializers.ModelSerializer):
    whether_following = serializers.SerializerMethodField('_whether_following')

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        return bool(obj.following_id.filter(user_id=my_id))
        
    class Meta:
        model = models.User
        fields = ('user_id','name','image_url','email','introduction','whether_following')


class UserFollowingDetailSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField(method_name='_followings', read_only=True)
    whether_following = serializers.SerializerMethodField('_whether_following')

    def _followings(self, obj):
        followings = models.User.objects.filter(
            user_id__in=models.Following.objects.filter(
                user=obj.user_id,
            ).values_list('user', flat=True)
        )
        return UserSimpleSerializer(followings, many=True).data

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        print("obj",obj.follower)
        return bool(obj.follower.filter(user_id=my_id))

    class Meta:
        model = models.Following
        fields = ('following_id','followings','whether_following')


class UserFollowerDetailSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField(method_name='_follower', read_only=True)

    def _follower(self, obj):
        user_id = self.context.get('user_id')
        followers = models.User.objects.filter(
            user_id__in=models.Following.objects.filter(
                follow_user=user_id,
            ).values_list('user', flat=True)
        )
        return UserSimpleSerializer(followers, many=True).data

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        print("obj",obj.follower)
        return bool(obj.follower.filter(user_id=my_id))

    class Meta:
        model = models.Following
        fields = ('following_id','follower')


class UserFollowingDetailSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField(method_name='_following', read_only=True)

    def _following(self, obj):
        user_id = self.context.get('user_id')
        followings = models.User.objects.filter(
            user_id__in=models.Following.objects.filter(
                user=user_id,
            ).exclude(follow_user__isnull=True).values_list('follow_user', flat=True)
        )
        return UserSimpleSerializer(followings, many=True).data

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        print("obj",obj.follower)
        return bool(obj.follower.filter(user_id=my_id))

    class Meta:
        model = models.Following
        fields = ('user','following')

