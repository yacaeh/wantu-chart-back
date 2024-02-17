from django.urls import path, include
from django.contrib import admin
from movies.views import movie_upload_from_csv, channel_upload_from_csv, episode_upload_from_csv, ChannelView, ChannelDetailView, LatestRateView,generate_video_view, list_created_files
import debug_toolbar
import app.views as views

urlpatterns = [
    path('api/v1/users', include('users.urls')),
    path("api/v1/movies", include("movies.urls")),
    path("api/v1/feeds", include("feed.urls")),
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/v1/notices', views.NoticeView.as_view()),
    path('api/v1/channels', ChannelView.as_view()),
    path('api/v1/channels/<int:channel_id>', ChannelDetailView.as_view()),
    path('api/v1/movie_upload', movie_upload_from_csv, name='movie_upload'),
    path('api/v1/channel_upload', channel_upload_from_csv, name='channel_upload'),
    path('api/v1/episode_upload', episode_upload_from_csv, name='episode_upload'),
    path('api/v1/latest-ratings', LatestRateView.as_view()),
    path('api/v1/common/reply', views.ReplyView.as_view(), name='reply'),
    path('api/v1/common/reply/<int:reply_id>', views.ReplyDetailView.as_view(), name='reply-detail'),
    path('api/v1/common/reply/<int:reply_id>/nested_reply', views.NestedReplyView.as_view(), name='nested-reply'),
    path('api/v1/common/reply/<int:reply_id>/nested_reply/<int:nested_reply_id>', views.NestedReplyDetailView.as_view(), name='nested-reply-detail'),
    path('api/v1/common/like', views.LikeView.as_view(), name='like'),
    path('api/v1/following', views.FollowingView.as_view(), name='following'),
    path('api/v1/following/<int:user_id>', views.FollowingUserDetailView.as_view(), name='following-user-detail'),
    path('api/v1/follower/<int:user_id>', views.FollowerUserDetailView.as_view(), name='follower-user-detail'),
    path('api/v1/generate_video', generate_video_view, name='generate_video'),
    path('api/v1/list-generate-video', list_created_files, name='list-generate-video'),   
]