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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tmp = {
            # 'sport': self.request.GET.get('sport'),
            'region': self.request.GET.get('region'),
            'lesson_type': self.request.GET.get('type'),
            # week_frequency = self.request.GET.get('week_frequency')
            'order': self.request.GET.get('order'),
            'is_search': self.request.GET.get('is_search'),
            'keyword': self.request.GET.get('keyword'),
        }
        context.update(tmp)
        return context

    def get_queryset(self):
        # sport = self.request.GET.get('sport')
        region = self.request.GET.get('region')
        lesson_type = self.request.GET.get('type')
        # week_frequency = self.request.GET.get('week_frequency')
        order = self.request.GET.get('order')
        is_search = self.request.GET.get('is_search')
        keyword = self.request.GET.get('keyword')

        lessons = Lesson.objects.none()

        if is_search:
            lessons = Lesson.objects.filter(
                Q(title__icontains=keyword) |
                Q(coach__name__icontains=keyword) |
                Q(academy__sport__name__icontains=keyword) |
                Q(academy__name__icontains=keyword))
        else :
            # if sport is None and region is None and \
            # lesson_type is None and week_frequency is None:
            if region is None and lesson_type is None:
                lessons = Lesson.objects.all()

            # if sport is not None:
            #     lessons = Lesson.objects.filter(sport=sport)
            if region is not None:
                for r in map(int, region):
                    tmp = Lesson.objects.filter(academy__small_district=r)
                    lessons = lessons.union(tmp)
            if lesson_type is not None:
                for t in lesson_type:
                    tmp = Lesson.objects.filter(lesson_type=t)
                    lessons = lessons.union(tmp)
            # if week_frequency is not None:
            #     for wf in map(int, week_frequency):
            #         tmp = Lesson.objects.filter(week_frequency=wf)
            #         lessons.union(tmp)

            if lessons:
                if order == "최신순":
                    lessons = lessons.order_by('-created_at')
                elif order == "평점 낮은 순":
                    lessons = lessons.order_by('rating')
                elif order == "평점 높은 순":
                    lessons = lessons.order_by('-rating')
                elif order == "가격 낮은 순":
                    lessons = lessons.order_by('price')
                elif order == "가격 높은 순":
                    lessons = lessons.order_by('-price')
                else:
                    lessons = lessons.order_by('-likes_count')
        return lessons


class LessonDetailView(DetailView):
    model = Lesson
    context_object_name = 'lesson'
    template_name = 'user/lesson_detail.html'


def sport_list(request):
    return render(request, 'user/sport_list.html')


class LikesTemplateView(TemplateView):
    template_name = 'user/likes.html'
