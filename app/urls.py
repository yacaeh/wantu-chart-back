from django.urls import path, include
from django.contrib import admin
from movies.views import movie_upload_from_csv, channel_upload_from_csv, episode_upload_from_csv, ChannelView, ChannelDetailView, LatestRateView
import debug_toolbar

urlpatterns = [
    path('api/v1/users', include('users.urls')),
    path("api/v1/movies", include("movies.urls")),
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/v1/channels', ChannelView.as_view()),
    path('api/v1/channels/<int:channel_id>', ChannelDetailView.as_view()),
    path('api/v1/movie_upload', movie_upload_from_csv, name='movie_upload'),
    path('api/v1/channel_upload', channel_upload_from_csv, name='channel_upload'),
    path('api/v1/episode_upload', episode_upload_from_csv, name='episode_upload'),
    path('api/v1/latest-ratings', LatestRateView.as_view()),
]