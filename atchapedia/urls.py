from django.urls import path, include
from django.contrib import admin
from movies.views import movie_upload_from_csv, channel_upload_from_csv, episode_upload_from_csv, ChannelView, ChannelDetailView

urlpatterns = [
    path('users', include('users.urls')),
    path("movies", include("movies.urls")),
    path('admin', admin.site.urls),
    path('channels', ChannelView.as_view()),
    path('channels/<int:channel_id>', ChannelDetailView.as_view()),
    path('movie_upload', movie_upload_from_csv, name='movie_upload'),
    path('channel_upload', channel_upload_from_csv, name='channel_upload'),
    path('episode_upload', episode_upload_from_csv, name='episode_upload'),
]