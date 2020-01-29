from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView

from core.views import HotLessonListView, RecentLessonListView, SportsDetailView, LessonDetailView, LikesTemplateView
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('sports_lists', views.sportlists, name='sportslists'),
    # path('login/', LoginView.as_view(), name='login'),
    path('', views.index, name='index'),
    # path('register/', RegistrationView.as_view(form_class=views.MyCustomUserForm, success_url='/'), name='django_registration_register'), # 메일인증없이 1 step
    path('register/', RegistrationView.as_view(success_url='/'), name='django_registration_register'), # 메일인증없이 1 step
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('hot_lessons/',HotLessonListView.as_view(), name='hot_lessons'),
    path('recent_lessons/',RecentLessonListView.as_view(), name='recent_lessons'),
    path('lessondetail/<int:pk>/', LessonDetailView.as_view(), name='lessondetail'),
    path('sportsdetail/<int:pk>/', SportsDetailView.as_view(), name='sportsdetail'),
    path('likes/', LikesTemplateView.as_view(), name='likes'),
    path('logout/', LogoutView.as_view(), name='logout'),
]