from typing import Any
from django.contrib import admin
from . import models
from users.models import User
from app.utils.youtube import get_channel_info, get_video_details, get_highlights, make_video_info_request, make_api_request, get_video_ids, process_playlist, API_KEY_LIST, API_INDEX,add_playlist_videos

@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "channel_id",
        "title",
        "handle",
        "thumbnail",
        "description",
        "published_at",
        "subscriber_count",
        "view_count",
        "video_count",
        "updated_at",
    )
class MovieGenreInline(admin.TabularInline):
    model = models.Movie.genre.through

class MovieCountryInline(admin.TabularInline):
    model = models.Movie.country.through

class MovieEpisodeInline(admin.TabularInline):
    model = models.Movie.episode.through

class MovieParticipantInline(admin.TabularInline):
    model = models.Movie.participant.through

# Register your models here.
@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "release_date",
        "description",
        "running_time",
        "poster_image",
        "trailer",
        "channel",
        "playlist",
        )
    inlines = [MovieGenreInline,MovieCountryInline,MovieEpisodeInline,MovieParticipantInline]
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        # Save other episodes...        
        super().save_model(request, obj, form, change)

        print("SAVE MODEL!!!")
        # Get channel info
        add_playlist_videos(obj.playlist)


@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "grade",
    )

@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "image_url",
    )

@admin.register(models.MovieParticipant)
class MovieParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "movie",
        "participant",
        "role",
    )

@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "movie",
        "rate",
        "comment",
    )

@admin.register(models.WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "movie",
    )

@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )

@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "link",
    )

@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "image_url",
        "title",
        "subtitle",
        "link",
        "type",
        "order"
    )