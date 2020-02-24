from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView

from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/', include('allauth.urls')),
    path('login/', views.CustomizedLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # 메일인증없이 1 step
    path('register/', RegistrationView.as_view(success_url='/'), name='django_registration_register'),
    # path('register/', RegistrationView.as_view(form_class=views.MyCustomUserForm, success_url='/'), name='django_registration_register'),

    path('lesson/list/', views.LessonListView.as_view(), name='lesson_list'),

    path('sport/list/', views.SportListView.as_view(), name='sport_list'),
    path('lesson/detail/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/list/liked', views.LikedLessonListView.as_view(), name='liked_lesson_list'),

    path('user/create/', views.user_create, name='user_create'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('lesson/like/', views.like_create_delete, name='like_create_delete'),
    path('review/delete/', views.review_delete, name='review_delete'),

]