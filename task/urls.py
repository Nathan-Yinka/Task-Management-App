from django.urls import path,reverse_lazy
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path("", views.TaskListView.as_view(), name="home"),
    path("api/", views.TaskListApiView.as_view(), name="task_list_create"),
    path("api/<int:pk>/", views.TaskRetreieveUpdateDeleteApiView.as_view(), name="task_update_retrieve_destroy"),
    path("auth/", views.AuthView.as_view(), name="auth"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy("auth")), name='logout'),
]
