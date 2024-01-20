from rest_framework import serializers
from movies.models import Rating
from users.models           import User, Reply
from app.models import Following
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','name','image_url','introduction')

class ReplySerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    nested_reply_cnt = serializers.SerializerMethodField('_nested_reply_cnt')
    like_cnt = serializers.SerializerMethodField('_like_cnt')
    whether_liked = serializers.SerializerMethodField('_whether_liked')
    report_cnt = serializers.SerializerMethodField('_report_cnt')
    whether_reported = serializers.SerializerMethodField('_whether_reported')

    def _nested_reply_cnt(self, obj):
        return obj.nestedreply_set.count()

    def _like_cnt(self, obj):
        return obj.like_set.count()

    def _whether_liked(self, obj):
        return bool(obj.like_set.filter(user_id=obj.id, reply_id=obj.reply_id))


    def _report_cnt(self, obj):
        return obj.report_set.count()

    def _whether_reported(self, obj):
        return bool(obj.report_set.filter(user_id=obj.id, reply_id=obj.reply_id))

    class Meta:
        model = Reply
        fields = ('reply_id','user','text','created_at','updated_at','nested_reply_cnt','like_cnt','whether_liked','report_cnt','whether_reported')



class RatingSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    reply_cnt = serializers.SerializerMethodField('_reply_cnt')
    like_cnt = serializers.SerializerMethodField('_like_cnt')
    whether_liked = serializers.SerializerMethodField('_whether_liked')
    # whether_reported = serializers.SerializerMethodField('_whether_reported')

    def _reply_cnt(self, obj):
        return obj.reply_set.count()

    def _like_cnt(self, obj):
        return obj.like_set.count()

    def _whether_liked(self, obj):
        return bool(obj.like_set.filter(user_id=obj.id, reply_id=obj.reply_id))


    # def _report_cnt(self, obj):
    #     return obj.report_set.count()

    # def _whether_reported(self, obj):
    #     return bool(obj.report_set.filter(user_id=obj.id, reply_id=obj.reply_id))

    class Meta:
        model = Rating
        fields = ('rating_id','rate','user','text','created_at','updated_at','nested_reply_cnt','like_cnt','whether_liked','report_cnt','whether_reported')


class UserSimpleFollowingSerializer(serializers.ModelSerializer):
    whether_following = serializers.SerializerMethodField('_whether_following')

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        return bool(obj.following_id.filter(user_id=my_id))
        
    class Meta:
        model = User
        fields = ('user_id','name','image_url','email','introduction','whether_following')


class UserFollowingDetailSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField(method_name='_followings', read_only=True)
    whether_following = serializers.SerializerMethodField('_whether_following')

    def _followings(self, obj):
        followings = User.objects.filter(
            user_id__in=Following.objects.filter(
                user=obj.id,
            ).values_list('user', flat=True)
        )
        return UserSimpleSerializer(followings, many=True).data

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        print("obj",obj.follower)
        return bool(obj.follower.filter(user_id=my_id))

    class Meta:
        model = Following
        fields = ('following_id','followings','whether_following')


class UserFollowerDetailSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField(method_name='_follower', read_only=True)

    def _follower(self, obj):
        user_id = self.context.get('user_id')
        followers = User.objects.filter(
            user_id__in=Following.objects.filter(
                follow_user=user_id,
            ).values_list('user', flat=True)
        )
        return UserSimpleSerializer(followers, many=True).data

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        print("obj",obj.follower)
        return bool(obj.follower.filter(user_id=my_id))

    class Meta:
        model = Following
        fields = ('following_id','follower')


class UserFollowingDetailSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField(method_name='_following', read_only=True)

    def _following(self, obj):
        user_id = self.context.get('user_id')
        followings = User.objects.filter(
            user_id__in=Following.objects.filter(
                user=user_id,
            ).exclude(follow_user__isnull=True).values_list('follow_user', flat=True)
        )
        return UserSimpleSerializer(followings, many=True).data

    def _whether_following(self, obj):
        my_id = self.context.get('my_id')
        print("obj",obj.follower)
        return bool(obj.follower.filter(user_id=my_id))

    class Meta:
        model = Following
        fields = ('user','following')

class UserDetailSerializer(serializers.ModelSerializer):
    # following = serializers.SerializerMethodField(method_name='_following', read_only=True)
    # follower = serializers.SerializerMethodField(method_name='_follower', read_only=True)
    # whether_following = serializers.SerializerMethodField('_whether_following')
    is_mine = serializers.SerializerMethodField('_is_mine')
    ratings = serializers.SerializerMethodField('_ratings')
    replies = serializers.SerializerMethodField('_replies')
    wishlist = serializers.SerializerMethodField('_wishlist')

    def _is_mine(self, obj):
        my_user = self.context.get('my_user')
        print("obj",obj.id, my_user.id)
        return obj.id == my_user.id
    
    def _ratings(self, obj):
        return obj.rating_set.count()
    
    def _replies(self, obj):
        return obj.reply_set.count()
    
    def _wishlist(self, obj):
        return obj.wishlist_set.count()

    # def _following(self, obj):
    #     followings = User.objects.filter(
    #         user_id__in=Following.objects.filter(
    #             user=obj.id,
    #         ).exclude(follow_user__isnull=True).values_list('follow_user', flat=True)
    #     )
    #     return UserSimpleSerializer(followings, many=True).data
    

    # def _follower(self, obj):
    #     followers = User.objects.filter(
    #         user_id__in=Following.objects.filter(
    #             follow_user=obj.id,
    #         ).exclude(user__isnull=True).values_list('user', flat=True)
    #     )
    #     return UserSimpleSerializer(followers, many=True).data

    # def _whether_following(self, obj):
    #     my_id = self.context.get('my_user_id')
    #     return bool(obj.follower.filter(user_id=my_id))

    class Meta:
        model = User
        fields = ('id','name','image_url','email','introduction','is_mine', 'ratings', 'replies', 'wishlist')
