from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexView, name="index"),
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("create", views.createGameView, name="create"),
    path("play/<int:id>", views.playGameView, name="play"),
    path("play/<int:id>/move/<int:position>", views.makeMoveView, name="move"),
    path("join/<int:id>", views.joinGameView, name="join"),
]
