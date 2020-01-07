from django.db import models
from django.contrib.auth.models import User, Group, UserManager
import tagulous.models


class Sport(models.Model):
    name = models.CharField(max_length=255, verbose_name='스포츠 명')

    class Meta:
        verbose_name = '스포츠'
        verbose_name_plural = '스포츠'

    def __str__(self):
        return self.name


class Academy(models.Model):
    name = models.CharField(max_length=255, verbose_name='업체 명')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='스포츠')
    introduction = models.TextField(blank=True, null=True, verbose_name='업체 소개')
    tel_num = models.CharField(max_length=255, verbose_name='업체 번호')
    email = models.EmailField(verbose_name='업체 이메일')

    class Meta:
        verbose_name = '업체'
        verbose_name_plural = '업체'

    def __str__(self):
        return str(self.sport.name) + str(self.name)


class Coach(models.Model):
    name = models.CharField(max_length=255, verbose_name='코치 이름')
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, verbose_name='소속 업체')
    introduction = models.TextField(blank=True, null=True, verbose_name='코치 소개')
    tel_num = models.CharField(max_length=255, verbose_name='코치 번호')
    email = models.EmailField(verbose_name='코치 이메일')

    class Meta:
        verbose_name = '코치'
        verbose_name_plural = '코치'

    def __str__(self):
        return str(self.academy.name) + '의' + str(self.name)


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='레슨 제목')
    academy = models.ForeignKey(Academy, null=True,on_delete=models.CASCADE, verbose_name='업체')
    coach = models.ForeignKey(Coach, null=True,on_delete=models.CASCADE, verbose_name='코치 명')
    price = models.IntegerField(verbose_name='정가')
    discount_price = models.IntegerField(verbose_name='할인가')
    start_datetime = models.DateTimeField(verbose_name='시작 날짜')
    end_datetime = models.DateTimeField(verbose_name='마감 날짜')

    class Meta:
        verbose_name = '레슨'
        verbose_name_plural = '레슨'

    def __str__(self):
        return str(self.academy.name) + '의 ' + str(self.title)