import datetime as dt
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.decorators.http import require_POST
from django.views.generic import (
    DetailView, ListView, CreateView,
    DeleteView)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.forms import *
from core.models import Lesson, Sport, BigDistrict, Like, Review, WrongInfo


class CustomizedLoginView(LoginView):
    form_class = CustomizedAuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(self, request, *args, **kwargs)


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
                Q(academy__name__icontains=keyword)|
                Q(academy__small_district__name__icontains=keyword)|
                Q(academy__small_district__big_district__name__icontains
                  =keyword)
            )
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            this_user = self.request.user
            likes = Like.objects.filter(liked_by=this_user, lesson=self.object).count()
            if likes > 0:
                context['likes'] = True
            else:
                context['likes'] = False
        reviews = Review.objects.filter(lesson=self.object)
        page = str(self.request.GET.get('page', 1))
        page = int(page.replace('/', ''))
        p = Paginator(reviews, 3)
        try:
            review_list = p.page(page)
        except PageNotAnInteger:
            review_list = p.page(1)
        except EmptyPage:
            review_list = p.page(p.num_pages)
        context['reviews'] = review_list
        return context


class SportListView(ListView):
    model = Sport
    context_object_name = 'sports'
    template_name = 'user/sport_list.html'


def user_create(request):
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('login')
    ctx = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/test_signup.html', ctx)


class ProfileCreateView(CreateView):
    model = Profile
    success_url = '/'
    form_class = ProfileForm
    template_name = 'user/profile_form.html'

    def get(self, request, *args, **kwargs):
        if Profile.objects.filter(user=request.user).exists():
            return redirect('index')
        return render(request, 'user/profile_form.html')

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('index')
        return render(request, 'user/profile_form.html')


class LikedLessonListView(ListView):
    model = Lesson
    template_name = 'user/liked_lesson_list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        likes = Like.objects.filter(liked_by=self.request.user)
        lesson_pk_list = []
        for like in likes:
            lesson_pk_list.append(like.lesson.pk)
        return Lesson.objects.filter(pk__in=lesson_pk_list)


@login_required
@require_POST
def like_create_delete(request):
    lesson = get_object_or_404(Lesson, pk=request.POST.get('lesson'))
    lesson_like, is_created = lesson.likes.get_or_create(
        liked_by=request.user)

    if is_created:
        msg = "수업 찜하기 완료"
    else :
        lesson_like.delete()
        msg = "수업 찜하기 취소"

    ctx ={
        'msg': msg,
    }
    return HttpResponse(json.dumps(ctx), content_type="application/json")


@login_required
@require_POST
def review_delete(request):
    review = Review.objects.get(id=int(request.POST['review_id']))
    if review.written_by_id == request.user.id:
        review.delete()
    return HttpResponse()


def create_update_review(request):
    lesson = get_object_or_404(Lesson, pk=request.POST.get('lesson'))
    review, is_created = lesson.reviews.get_or_create(
        written_by=request.user)

    if is_created:
        pass
    else:
        pass




def create_wrong_info(request):
    try:
        phone_num, content = request.POST['phone_num'], request.POST['content']
        wrong_info = WrongInfo.objects.create(phone_num=phone_num, content=content)
        wrong_info.save()
    except:
        if request.POST['submit_type'] == '1':
            new_review = Review.objects.create(
                lesson_id=request.POST.get['pk'],
                written_by=request.user,
                rating=int(request.POST.get('rates', 0)),
                comment=request.POST['comment']
            )
            new_review.save()
        else:
            review = Review.objects.get(id=int(request.POST['review_id']))
            if review.written_by == request.user:
                review.rating = int(request.POST['rates'])
                review.comment = request.POST['comment']
                review.save()