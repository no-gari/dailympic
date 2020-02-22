"""dailympic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:i
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import re

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from board.views import upload_attachment
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

from django.views.static import serve
from django.urls import re_path
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('community/', include('board.urls'), name='community'),
    url(r'^summernote/upload_attachment/$', upload_attachment, name='django_summernote-upload_attachment'),
    path('summernote/', include('django_summernote.urls')),
    # path('',include('social_django.urls', namespace='social'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
