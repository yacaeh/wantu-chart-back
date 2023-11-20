from django.urls import path

from users.views import Login, SignUpView, RatingsView, WishlistView, MyRatingsView, MyWishlistView, Profile, MyPlayHistoryView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', Login.as_view()),
    path("/<int:user_id>/ratings", RatingsView.as_view()),
    path("/myratings", MyRatingsView.as_view()),
    path('/<int:user_id>/wishlist', WishlistView.as_view()),
    path("/mywishlist", MyWishlistView.as_view()),
    path('/playhistory', MyPlayHistoryView.as_view()),
    path("/<int:user_id>", Profile.as_view()),
]
