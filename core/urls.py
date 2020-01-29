from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView

from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('sports_lists', views.sportlists, name='sportslists'),
    # path('login/', LoginView.as_view(), name='login'),
    path('', views.index, name='index'),
    # path('register/', RegistrationView.as_view(form_class=views.MyCustomUserForm, success_url='/'), name='django_registration_register'), # 메일인증없이 1 step
    path('register/', RegistrationView.as_view(success_url='/'), name='django_registration_register'), # 메일인증없이 1 step
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
]