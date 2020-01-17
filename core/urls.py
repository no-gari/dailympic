from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('sports_lists', views.sportlists, name='sportslists'),
    path('login/', LoginView.as_view(), name='login'),
    path('', views.index, name='index'),
]