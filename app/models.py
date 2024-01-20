from django.db import models
from django.db.models.deletion import SET_DEFAULT
from users.models import User, Reply, NestedReply
from movies.models import Movie, Channel, Episode, Rating

class Notice(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    type= models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notices"

class Hashtag(models.Model):
    hashtag_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'hashtag'


class Feed(models.Model):
    feed_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    hashtag = models.ManyToManyField(Hashtag, blank=True, through='FeedHashtag')
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.TextField(blank=True, null=True)
    image_urls = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feed'

class FeedHashtag(models.Model):
    feed_hashtag_id = models.AutoField(primary_key=True)
    feed = models.ForeignKey(Feed, models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, models.CASCADE)

    class Meta:
        managed = True
        db_table = 'feed_hashtag'
        

class Like(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    feed = models.ForeignKey(Feed, models.CASCADE, null=True, blank=True)
    rating = models.ForeignKey(Rating, models.CASCADE, null=True, blank=True)
    reply = models.ForeignKey(Reply, models.CASCADE, blank=True, null=True)
    nested_reply = models.ForeignKey(NestedReply, models.CASCADE, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'like'



class Following(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='follower_id')
    follow_user = models.ForeignKey(User, models.CASCADE, related_name='following_id', blank=True, null=True)
    hashtag = models.ForeignKey(Hashtag, models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'following'
