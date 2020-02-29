import django_filters
from django.utils import timezone
from django.db.models import F, Sum, Count, Case, When, Q
from datetime import date, datetime, timedelta
from . import models

class BoardListFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='제목')
    user = django_filters.CharFilter(method='filter_user', label='글쓴이')
    
    def filter_user(self, queryset, name, value):
        return queryset.filter(user__username=value).order_by('-id')