from django.urls import path
import feed.views as views


urlpatterns = [
    path('', views.FeedView.as_view(), name='feed'),
    path('/user/<int:user_id>', views.UserFeedView.as_view(), name='feed-user'),
    path('/<int:feed_id>', views.FeedDetailView.as_view(), name='feed-detail'),
]
