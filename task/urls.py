from django.urls import path
from . import views


urlpatterns = [
    path("", views.TaskListView.as_view(), name="home"),
    path("auth/", views.AuthView.as_view(), name="auth"),
]
