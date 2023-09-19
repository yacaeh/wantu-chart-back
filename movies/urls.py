from django.urls  import path

from movies.views import RateView, GenreMovieView, MovieView, MovieDetailView, CommentView, EpisodeMovieView, cached, cacheless

urlpatterns = [
    path("",MovieView.as_view()),
    path('/<int:movie_id>', MovieDetailView.as_view()),
    path('/<int:movie_id>/user-rate', RateView.as_view()),
    path("/<int:movie_id>/comments",CommentView.as_view()),
    path('/related-movies', GenreMovieView.as_view()),
    path('/<int:movie_id>/episodes', EpisodeMovieView.as_view()),
    path('/cached', cached),
    path('/cacheless', cacheless)
]
