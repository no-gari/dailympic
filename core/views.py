from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
import datetime as dt
from core.models import Lesson


def index(request):
    hot_lessons = Lesson.objects.order_by('-like_count')[:3]
    recent_lessons = Lesson.objects.filter(
        created_at__gte=dt.datetime.today() - dt.timedelta(days=14)
    ).order_by('-create_at')[:3]
    ctx = {
        'hot_lessons' : hot_lessons,
        'recent_lessons' : recent_lessons,
    }
    return render(request, './user/index.html')


class HotLessonListView(ListView):
    model = Lesson
    paginate_by = 20
    # template_name='/templates/user/read_lessons.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        return Lesson.objects.order_by('-like_count')


class RecentLessonListView(ListView):
    model = Lesson
    paginate_by = 20
    # template_name='/templates/user/read_lessons.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        return Lesson.objects.order_by('-created_at')


class OneDayLessonListView(ListView):
    model = Lesson
    paginate_by = 20
    # template_name='/templates/user/read_lessons.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        return Lesson.objects.filter(lesson_type='ONE_DAY').order_by('-hits')


def login(request):
    return render(request, "./user/login.html")

