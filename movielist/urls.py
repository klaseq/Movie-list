from django.urls import path
from . import views
from . import url_handlers

urlpatterns = [
    path("movie_index/", views.MovieIndex.as_view(), name="movie_index"),
    path("<int:pk>/movie_detail/", views.CurrentMovieView.as_view(), name="movie_detail"),
    path("create_movie/", views.CreateMovie.as_view(), name="new_movie"),
    path("register/", views.UserViewRegister.as_view(), name="register"),
    path("login/", views.UserViewLogin.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("<int:pk>/edit/", views.EditMovie.as_view(), name="edit_movie"),
    path("", url_handlers.index_handler)
]