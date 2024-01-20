import app.models as models
import users.models as user_models
from rest_framework import serializers
from users.serializers import UserSimpleSerializer

class FeedSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feed
        fields = ('__all__')


class ReplySerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    nested_reply_cnt = serializers.SerializerMethodField('_nested_reply_cnt')
    like_cnt = serializers.SerializerMethodField('_like_cnt')
    whether_liked = serializers.SerializerMethodField('_whether_liked')
    label = serializers.SerializerMethodField('_label')

    def _nested_reply_cnt(self, obj):
        return obj.nestedreply_set.count()

    def _like_cnt(self, obj):
        return obj.like_set.count()

    def _whether_liked(self, obj):
        return bool(obj.like_set.filter(user_id=obj.user_id, reply_id=obj.reply_id))

    def _label(self, obj):
        if obj.user_id == models.Feed.objects.get(feed_id=obj.feed_id).user_id:
            return "creator"
        elif bool(models.Investment.objects.filter(user_id=obj.user_id, feed_id=obj.feed_id)):
            return "investors"
        else:
            return "visitors"

    class Meta:
        model = models.Reply
        fields = ('reply_id','user','text','created_at','updated_at','nested_reply_cnt','like_cnt','whether_liked','label')


class NestedReplySerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    like_cnt = serializers.SerializerMethodField('_like_cnt')
    whether_liked = serializers.SerializerMethodField('_whether_liked')
    label = serializers.SerializerMethodField('_label')

    def _nested_reply_cnt(self, obj):
        return obj.nestedreply_set.count()

    def _like_cnt(self, obj):
        return obj.like_set.count()

    def _whether_liked(self, obj):
        user_id = self.context.get('user_id')
        return bool(obj.like_set.filter(user_id=user_id, nested_reply_id=obj.nested_reply_id))

    def _label(self, obj):
        if obj.user_id == models.Feed.objects.get(feed_id=(models.Reply.objects.get(reply_id=obj.reply_id).feed_id)).user_id:
            return "creator"
        elif bool(models.Investment.objects.filter(user_id=obj.user_id, feed_id=(models.Reply.objects.get(reply_id=obj.reply_id).feed_id))):
            return "investors"
        else:
            return "visitors"

    class Meta:
        model = models.NestedReply
        fields = ('nested_reply_id','user','text','created_at','updated_at','like_cnt','whether_liked','label')


class ReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reply
        fields = '__all__'


class NestedReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NestedReply
        fields = '__all__'


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = '__all__'


class FollowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Following
        fields = '__all__'


class UserSimpleFollowingSerializer(serializers.ModelSerializer):
    whether_following = serializers.SerializerMethodField('_whether_following')

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        return bool(obj.following_id.filter(user_id=my_id))
        
    class Meta:
        model = user_models.User
        fields = ('user_id','name','image_url','email','introduction','whether_following')


class UserFollowingDetailSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField(method_name='_followings', read_only=True)
    whether_following = serializers.SerializerMethodField('_whether_following')

    def _followings(self, obj):
        followings = user_models.User.objects.filter(
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
        followers = user_models.User.objects.filter(
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
        followings = user_models.User.objects.filter(
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

