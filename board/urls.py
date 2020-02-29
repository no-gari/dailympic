from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'board'
urlpatterns = [
    path('<str:mid>', views.BoardListView.as_view(), name='board_list'),
    path('board_detail/<int:pk>', views.BoardDetailView.as_view(), name='board_detail'),
    path('document_add/<str:mid>', views.DocumentCreateView.as_view(), name='document_add'),
    path('document_edit/<int:pk>', views.DocumentUpdateView.as_view(), name='document_edit'),
    path('document_delete/<int:pk>', views.DocumentDeleteView.as_view(), name='document_delete'),
    url(r'^file_download/(?P<pk>[0-9]+)/$', views.file_download, name='file_download'),
    url(r'^set_file_delete/$', views.set_file_delete, name='set_file_delete'),
    url(r'^summernote/upload_attachment/$', views.upload_attachment, name='django_summernote-upload_attachment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
