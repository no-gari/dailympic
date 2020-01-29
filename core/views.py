from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
import datetime as dt
from core.models import Lesson, Sport


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


class LessonDetailView(DetailView):
    model=Lesson
    context_object_name = 'lesson'
    template_name = 'user/lesson_detail.html'


class SportsDetailView(DetailView):
    model = Sport
    paginate_by=20
    context_object_name = 'sport'
    template_name = 'user/sports_detail.html'


def sportlists(request):
    return render(request, 'user/sportslists.html')


def login(request):
    return render(request, 'user/test_login.html')


def search(request):
    q = request.GET.get('q', "")
    lessons = Lesson.objects.filter(Q(title__icontains=q)|Q(coach__name__icontains=q))


class LikesTemplateView(TemplateView):
    template_name = 'user/likes.html'

