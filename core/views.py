from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, TemplateView, CreateView
import datetime as dt

from core.forms import *
from core.models import Lesson, Sport, BigDistrict


def login(request):
    return render(request, 'user/test_login.html')


def index(request):
    hot_lessons = Lesson.objects.order_by('-likes_count')[:4]
    recent_lessons = Lesson.objects.filter(
        created_at__gte=dt.datetime.today() - dt.timedelta(days=14)
    ).order_by('-created_at')[:4]
    ctx = {
        'hot_lessons': hot_lessons,
        'recent_lessons': recent_lessons,
    }
    return render(request, './user/index.html', ctx)


class LessonListView(ListView):
    model = Lesson
    context_object_name = 'lessons'
    template_name = 'user/lesson_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tmp = {
            'sports': Sport.objects.all(),
            'districts': BigDistrict.objects.all(),
            'sport': self.request.GET.get('sport'),
            'region': self.request.GET.get('region'),
            'lesson_type': self.request.GET.get('type'),
            'week_frequency': self.request.GET.get('week_frequency'),
            'order': self.request.GET.get('order'),
            'is_search': self.request.GET.get('is_search'),
            'keyword': self.request.GET.get('keyword'),
        }
        context.update(tmp)
        return context

    def get_queryset(self):
        sport = self.request.GET.get('sport')
        region = self.request.GET.get('region')
        lesson_type = self.request.GET.get('type')
        week_frequency = self.request.GET.get('week_frequency')
        order = self.request.GET.get('order')
        is_search = self.request.GET.get('is_search')
        keyword = self.request.GET.get('keyword')

        lessons = Lesson.objects.none()
        if is_search == 'true':
            is_search = True
        else:
            is_search = False

        if is_search:
            lessons = Lesson.objects.filter(
                Q(title__icontains=keyword) |
                Q(coach__name__icontains=keyword) |
                Q(academy__sport__name__icontains=keyword) |
                Q(academy__name__icontains=keyword))
        else:
            lessons = Lesson.objects.all()
            # lessons= Lesson.objects.none()

            if sport is not None and sport is not '':
                lessons = lessons.filter(academy__sport=int(sport))

            if region is not None and region is not '':
                region = region.split(',')
                tmp_lessons = Lesson.objects.none()
                for r in map(int, region):
                    tmp = lessons.filter(academy__small_district=r)
                    tmp_lessons = tmp_lessons.union(tmp)
                lessons = tmp_lessons

            if lesson_type is not None and lesson_type is not '':
                lesson_type = lesson_type.split(',')
                tmp_lessons = Lesson.objects.none()
                for t in lesson_type:
                    tmp = lessons.filter(lesson_type=t)
                    tmp_lessons = tmp_lessons.union(tmp)
                lessons = tmp_lessons

            if week_frequency is not None and week_frequency is not '':
                week_frequency = week_frequency.split(',')
                tmp_lessons = Lesson.objects.none()
                for wf in map(int, week_frequency):
                    tmp = lessons.filter(week_frequency=wf)
                    tmp_lessons = tmp_lessons.union(tmp)
                lessons = tmp_lessons

            if lessons:
                if order == "최신순":
                    lessons = lessons.order_by('-created_at')
                elif order == "평점 낮은 순":
                    lessons = lessons.order_by('rating')
                elif order == "평점 높은 순":
                    lessons = lessons.order_by('-rating')
                elif order == "가격 낮은 순":
                    lessons = lessons.order_by('org_price')
                elif order == "가격 높은 순":
                    lessons = lessons.order_by('-org_price')
                else:
                    lessons = lessons.order_by('-likes_count')
        return lessons


class LessonDetailView(DetailView):
    model = Lesson
    context_object_name = 'lesson'
    template_name = 'user/lesson_detail.html'


class SportListView(ListView):
    model = Sport
    context_object_name = 'sports'
    template_name = 'user/sport_list.html'


class LikesTemplateView(TemplateView):
    template_name = 'user/likes.html'


def user_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    ctx = {
        'user_form': UserForm(),
        'profile_form': ProfileForm(),
    }
    return render(request, 'user/test_signup.html', ctx)


class ProfileCreateView(CreateView):
    model = Profile
    success_url = '/'
    form_class = ProfileForm
    template_name = 'user/profile_form.html'

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('index')
        return render(request, 'user/user_create_fail.html', {
            'profile_form_errors': profile_form.errors,
        })


@login_required
def likes_list(request):
    render('user/likes.html', {
        'likes': request.user.likes,
    })
