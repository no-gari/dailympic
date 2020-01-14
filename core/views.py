from django.shortcuts import render

from core.models import Lesson


def index(request):
    hot_lessons = Lesson.objects.order_by('-hits')[:5]


    return render(request, '../templates/user/index.html')