from django.db import models
from movies.models import *
from app.models import *
class User(models.Model):

    name         = models.CharField(max_length=45)
    email        = models.EmailField(max_length=45)
    password     = models.CharField(max_length=500)
    introduction = models.CharField(max_length=100)
    image_url    = models.URLField(max_length=500, null=True)
    google_token = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name


# class Feed(models.Model):
#     user = models.ForeignKey('User', models.CASCADE)
#     rating = models.ForeignKey('movies.Rating', models.CASCADE, null=True, blank=True)
#     reply = models.ForeignKey('Reply', models.CASCADE, null=True, blank=True)
#     hashtag = models.ForeignKey('Hashtag', models.CASCADE, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         managed = True
#         db_table = 'feed'

class Reply(models.Model):
    rating = models.ForeignKey('movies.Rating', models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('User', models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    feed = models.ForeignKey('app.Feed', models.CASCADE, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'reply'




class NestedReply(models.Model):
    nested_reply_id = models.AutoField(primary_key=True)
    reply = models.ForeignKey('Reply', models.CASCADE)
    user = models.ForeignKey('User', models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'nested_reply'

