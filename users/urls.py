from django.urls import path

from users.views import Login, SignUpView, RatingsView, WishlistView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', Login.as_view()),
    path("/ratings/<int:user_id>", RatingsView.as_view()),
    path('/wishlist/<int:user_id>', WishlistView.as_view()),
]
