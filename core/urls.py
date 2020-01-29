from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView

from core.views import HotLessonListView, RecentLessonListView, SportsDetailView, LessonDetailView, LikesTemplateView
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/', include('allauth.urls')),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # 메일인증없이 1 step
    path('register/', RegistrationView.as_view(success_url='/'), name='django_registration_register'),
    # path('register/', RegistrationView.as_view(form_class=views.MyCustomUserForm, success_url='/'), name='django_registration_register'),

    path('sport_list', views.sport_list, name='sport_list'),
    path('hot_lessons/',HotLessonListView.as_view(), name='hot_lessons'),
    path('recent_lessons/',RecentLessonListView.as_view(), name='recent_lessons'),
    path('lesson_detail/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('sport_detail/<int:pk>/', SportsDetailView.as_view(), name='sport_detail'),
    path('likes/', LikesTemplateView.as_view(), name='likes'),
]