from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView

from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/login/', views.redirect_login(), name='redirect-login')
    path('login/', views.CustomizedLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', RegistrationView.as_view(success_url='/'), name='django_registration_register'),
    # path('register/', RegistrationView.as_view(form_class=views.MyCustomUserForm, success_url='/'), name='django_registration_register'),

    path('lesson/list/', views.LessonListView.as_view(), name='lesson_list'),

    path('sport/list/', views.SportListView.as_view(), name='sport_list'),
    # path('sport/detail/<int:pk>', views.SportDetailView.as_view(), name='sport_detail'),
    path('lesson/detail/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/list/liked', views.LikedLessonListView.as_view(), name='liked_lesson_list'),

    path('user/create/', views.user_create, name='user_create'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_update'),

    path('like/create_delete/', views.like_create_delete, name='like_create_delete'),

    path('review/delete/', views.review_delete, name='review_delete'),
    path('review/create_update/', views.review_create_update, name='review_create_update'),

    path('wronginfo/create/', views.wronginfo_create, name='wronginfo_create'),

]
