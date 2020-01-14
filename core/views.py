from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from core.models import Lesson


def index(request):
    hot_lessons = Lesson.objects.order_by('-hits')[:3]
    recent_lessons = Lesson.objects.order_by('-create_at')[:3]
    ctx = {
        'hot_lessons' : hot_lessons,
        'recent_lessons' : recent_lessons,
    }
    return render(request, '../templates/user/index.html')


class HotLessonListView(ListView):
    model = Lesson
    paginate_by = 20
    # template_name='/templates/user/read_lessons.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        return Lesson.objects.order_by('-hits')


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


