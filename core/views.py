from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
import datetime as dt
from core.models import Lesson, Sport


def login(request):
    return render(request, 'user/test_login.html')


def index(request):
    hot_lessons = Lesson.objects.order_by('-like_count')[:4]
    recent_lessons = Lesson.objects.filter(
        created_at__gte=dt.datetime.today() - dt.timedelta(days=14)
    ).order_by('-create_at')[:4]
    ctx = {
        'hot_lessons' : hot_lessons,
        'recent_lessons' : recent_lessons,
    }
    return render(request, './user/index.html', ctx)


class LessonListView(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'user/lesson_list.html'

    def get_queryset(self):
        region = self.kwargs.get('region')
        lesson_type = self.kwargs.get('type')
        # week_frequency = self.kwargs.get('week_frequency')
        order = self.kwargs.get('order')
        is_search = self.kwargs.get('is_search')
        keyword = self.kwargs.get('keyword')

        lessons = None

        if is_search:
            lessons = Lesson.objects.filter(
                Q(title__icontains=keyword) |
                Q(coach__name__icontains=keyword) |
                Q(academy__sport__name__icontains=keyword))
        else :
            # if region is None and lesson_type is None and week_frequency is None and order is None:
            if region is None and lesson_type is None and order is None:
                lessons = Lesson.objects.all()

            if region is not None:
                for r in region:
                    tmp = Lesson.objects.filter(academy__small_district=r)
                    lessons.union(tmp)
            if lesson_type is not None:
                for t in lesson_type:
                    tmp = Lesson.objects.filter(lesson_type=t)
                    lessons.union(tmp)
            # if week_frequency is not None:
            #     for wf in week_frequency:
            #         tmp = Lesson.objects.filter(week_frequency=wf)
            #         lessons.union(tmp)

            if lessons is not None:
                if order == "최신순" :
                    lessons = lessons.order_by('-created_at')
                elif order == "평점 낮은 순" :
                    lessons = lessons.order_by('-rating')
                elif order == "평점 높은 순" :
                    lessons = lessons.order_by('rating')
                else :
                    lessons = lessons.order_by('likes_count')
        return lessons


class LessonDetailView(DetailView):
    model = Lesson
    context_object_name = 'lesson'
    template_name = 'user/lesson_detail.html'


class SportsDetailView(DetailView):
    model = Sport
    paginate_by=20
    context_object_name = 'sport'
    template_name = 'user/sports_detail.html'


def sport_list(request):
    return render(request, 'user/sport_list.html')


class LikesTemplateView(TemplateView):
    template_name = 'user/likes.html'
