from django.urls  import path

from movies.views import RateView, GenreMovieView, MovieView, MovieDetailView, CommentView, EpisodeMovieView, WishListView, LatestRateView, RankingView , PlayHistoryView, MainTopRankView, list_created_files, download_file

urlpatterns = [
    path("",MovieView.as_view()),
    path("/rankings", RankingView.as_view()),
    path("/main-top-rankings", MainTopRankView.as_view()),
    path('/<int:movie_id>', MovieDetailView.as_view()),
    path('/<int:movie_id>/user-rate', RateView.as_view()),
    path("/<int:movie_id>/comments",CommentView.as_view()),
    path('/<int:movie_id>/wishlist', WishListView.as_view()),
    path('/related-movies', GenreMovieView.as_view()),
    path('/<int:movie_id>/episodes', EpisodeMovieView.as_view()),
    path('/<int:movie_id>/playhistory', PlayHistoryView.as_view()),
    path('list-files/', list_created_files, name='list_created_files'),
    path('download/<str:directory>/<str:filename>/', download_file, name='download_file'),
]
