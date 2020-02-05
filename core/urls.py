from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView

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

    path('lesson_list/', views.LessonListView.as_view(), name='lesson_list'),

    path('sport_list/', views.SportListView.as_view(), name='sport_list'),
    path('lesson_detail/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    # path('sport_detail/<int:pk>/', views.SportsDetailView.as_view(), name='sport_detail'),
    path('likes/', views.LikesTemplateView.as_view(), name='likes'),
]