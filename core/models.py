from django.db import models
from django.contrib.auth.models import User, Group, UserManager
import tagulous.models


class Sport(models.Model):
    name = models.CharField(max_length=255, verbose_name='종목명')
    icon = models.ImageField(default=None, blank=True)

    class Meta:
        verbose_name = '종목'
        verbose_name_plural = '스포츠'

    def __str__(self):
        return self.name


class Academy(models.Model):
    name = models.CharField(max_length=255, verbose_name='업체명')
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, verbose_name='종목', related_name='academies')
    introduction = models.TextField(blank=True, null=True, verbose_name='업체 소개')
    tel_num = models.CharField(max_length=255, verbose_name='업체 문의번호')
    email = models.EmailField(verbose_name='업체 이메일')

    class Meta:
        verbose_name = '업체'
        verbose_name_plural = '업체'

    def __str__(self):
        return str(self.sport.name) + str(self.name)


class Coach(models.Model):
    name = models.CharField(max_length=255, verbose_name='코치 이름')
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, verbose_name='소속 업체', related_name='coaches')
    introduction = models.TextField(blank=True, null=True, verbose_name='코치 소개')
    tel_num = models.CharField(max_length=255, verbose_name='코치 번호')
    email = models.EmailField(verbose_name='코치 이메일')

    class Meta:
        verbose_name = '코치'
        verbose_name_plural = '코치'

    def __str__(self):
        return str(self.academy.name) + '의' + str(self.name)


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='레슨명')
    academy = models.ForeignKey(Academy, null=True, on_delete=models.CASCADE, related_name='lessons')
    coach = models.ForeignKey(Coach, null=True, on_delete=models.CASCADE, related_name='lessons')
    price = models.IntegerField(verbose_name='정가')
    discount_rate = models.FloatField(verbose_name='할인율')
    start_date = models.DateField(verbose_name='시작일')
    end_date = models.DateField(verbose_name='종료일')

    class Meta:
        verbose_name = '레슨'
        verbose_name_plural = '레슨'

    def __str__(self):
        return str(self.academy.name) + '의 ' + str(self.title)


class District (models.Model):
    name = models.CharField(max_length=20, verbose_name='지역')
    icon = models.ImageField(default=None, blank=True)


class Location (models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='locations')
    lati = models.FloatField()
    long = models.FloatField()
    address = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, null=True, on_delete=models.SET_NULL, blank=True)

