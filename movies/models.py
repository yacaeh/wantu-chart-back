from django.db import models
from django.db.models.deletion import SET_DEFAULT
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class Channel(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    title = models.CharField(max_length=100)
    handle = models.CharField(max_length=100, null=True)
    channel_id = models.CharField(max_length=100, null=True)
    description = models.TextField(default="등록된 소개글이 없습니다.")
    published_at = models.DateTimeField(null=True)
    thumbnail = models.URLField(max_length=500)
    subscriber_count = models.BigIntegerField(blank=True, null=True, default=0)
    view_count = models.BigIntegerField(blank=True, null=True, default=0)
    video_count = models.BigIntegerField(blank=True, null=True, default=0)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)

    class Meta:
        db_table = "channels"

    def __str__(self):
        return self.title

class Movie(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    title          = models.CharField(max_length=100) 
    release_date   = models.DateField( blank=True, null=True)
    description    = models.TextField(default="", null=True, blank=True)
    running_time   = models.IntegerField( blank=True, null=True, default=0)
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, default=0.0)
    total_views = models.BigIntegerField(null=True, default=0) # This is the one that daily updated
    total_likes = models.BigIntegerField(null=True, default=0) # This is the one that daily updated
    total_comments = models.BigIntegerField(null=True, default=0) # This is the one that daily updated
    total_videos = models.BigIntegerField(null=True, default=0) # This is the one that daily updated
    total_dislikes = models.BigIntegerField(null=True, default=0) # This is the one that daily updated
    is_new = models.BooleanField(default=False, null=True, blank=True)
    wantu_score = models.BigIntegerField(null=True, default=0) # This is the one that daily updated => Sort by this value as ranking
    poster_image   = models.URLField(max_length=500, blank=True, null=True)
    trailer        = models.CharField(max_length=500, null=True)
    participant    = models.ManyToManyField("Participant", through="MovieParticipant")
    user_rating    = models.ManyToManyField('users.User', through="Rating", related_name="rater")
    user_wish      = models.ManyToManyField('users.User', through="WishList", related_name="wisher")
    genre          = models.ManyToManyField("Genre", through="MovieGenre")
    country        = models.ManyToManyField("Country", through="MovieCountry")
    episode       = models.ManyToManyField("Episode", through="MovieEpisode")
    channel       = models.ForeignKey("Channel", on_delete=models.CASCADE, null=True, blank=True)
    playlist    = models.CharField(max_length=500, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True,blank=True, null=True)

    class Meta:
        db_table = "movies"

    def __str__(self):
        return self.title

class Grade(models.Model):
    grade = models.CharField(max_length=45)
    
    class Meta:
        db_table = "grades"

    def __str__(self):
        return self.grade

class Participant(models.Model):
    name      = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500)

    class Meta:
        db_table = "participants"

    def __str__(self):
        return self.name

class MovieParticipant(models.Model):
    movie       = models.ForeignKey("Movie", on_delete=models.CASCADE)
    participant = models.ForeignKey("Participant", on_delete=models.CASCADE)
    role        = models.CharField(max_length=10)

    class Meta:
        db_table = "movie_participants"


class Rating(models.Model):
    user    = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL)
    movie   = models.ForeignKey("Movie", on_delete=models.CASCADE)
    rate    = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.CharField(max_length=1000)
    spoiler = models.BooleanField(default=False)

    class Meta:
        db_table = "ratings"


class WishList(models.Model):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    movie        = models.ForeignKey("Movie", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "wish_lists"


class Genre(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "genres"

    def __str__(self):
        return self.name


class MovieGenre(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)

    class Meta:
        db_table = "movie_genres"


class Episode(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(default="등록된 소개글이 없습니다.")
    release_date = models.DateField()
    link = models.CharField(max_length=500)
    viewCount = models.BigIntegerField(blank=True, null=True, default=0)
    likeCount = models.BigIntegerField(blank=True, null=True, default=0)
    dislikeCount = models.BigIntegerField(blank=True, null=True, default=0)
    commentCount = models.BigIntegerField(blank=True, null=True, default=0)
    duration = models.CharField(max_length=500, null=True, blank=True)
    highlights = models.JSONField(blank=True, null=True)
    topComments = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "episodes"

    def __str__(self):
        return self.name

class MovieEpisode(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE)

    class Meta:
        db_table = "movie_episodes"

class Image(models.Model):
    image_url = models.URLField(max_length=500)
    movie     = models.ForeignKey("Movie", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"


class Country(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "countries"

    def __str__(self):
        return self.name


class MovieCountry(models.Model):
    movie   = models.ForeignKey("Movie", on_delete=models.CASCADE)
    country = models.ForeignKey("Country", on_delete=models.CASCADE)

    class Meta:
        db_table = "movie_countries"
        

class Banner(models.Model):
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500)
    link = models.CharField(max_length=500)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    order = models.IntegerField()
    type = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "banners"

class Point(models.Model):
    amount = models.IntegerField(blank=True, null=True, default=0)
    user = models.ForeignKey('users.User', models.CASCADE) 
    type = models.CharField(max_length=255, blank=True, null=True) # 이벤트로 쌓인 포인트인지, 영상 시청으로 쌓인 포인트인지 구분
    type_id = models.CharField(max_length=255, blank=True, null=True) # 이벤트면 event_id, 레퍼럴이면 feed_id 혹은 episode_id
    status = models.CharField(max_length=255, blank=True, null=True) # 적립(EARNED)인지, 사용(USED)인지?
    start_at = models.DateTimeField(null=True) # 이벤트인 경우 start_at과 created_at이 다를 수 있음
    end_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'points'

class PlayHistory(models.Model):
    user    = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL)
    movie   = models.ForeignKey("Movie", on_delete=models.CASCADE)
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE)
    last_played = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-last_played']
        db_table = "play_histories"

# Rank model should contain the following fields (rank, rankFluc, movie Id, movie title, movie poster, wantu_score)

class DailyRank(models.Model):
    rank = models.JSONField(blank=True, null=True)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "daily_ranks"

class WeeklyRank(models.Model):
    rank = models.JSONField(blank=True, null=True)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "weekly_ranks"

class MonthlyRank(models.Model):
    rank = models.JSONField(blank=True, null=True)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "monthly_ranks"

class DailyView(models.Model):
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE)
    views = models.IntegerField()
    likes = models.IntegerField()
    comments = models.IntegerField()
    dislikes = models.IntegerField()
    date = models.DateField()
    class Meta:
        managed = True
        db_table = "daily_views"

# https://api.playboard.co/v1/chart/channel?locale=ko&countryCode=KR&period=1700265600&size=20&chartTypeId=10&periodTypeId=2&indexDimensionId=10&indexTypeId=3&indexTarget=cooking&indexCountryCode=KR
