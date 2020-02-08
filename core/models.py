from django import template
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


register = template.Library()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        default=None,null=True,blank=True,verbose_name='프로필 사진'
    )
    name = models.CharField(max_length=31, verbose_name='이름'),
    SEX_CHOICES = (
        ('M', '남'),
        ('W', '여')
    )
    sex = models.CharField(max_length=7, choices=SEX_CHOICES, verbose_name='성별'),
    birthday = models.DateField(verbose_name='생년월일')
    phone = models.CharField(max_length=31, null=True, blank=True, verbose_name='휴대전화')

    def __str__(self):
        return self.user.username


class Sport(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='종목명',
    )
    icon = models.ImageField(default=None, null=True, blank=True,)

    class Meta:
        verbose_name = '종목'
        verbose_name_plural = '스포츠'

    def __str__(self):
        return self.name


class BigDistrict (models.Model):
    # 서울시 마포구
    name = models.CharField(
        max_length=31, verbose_name='시군구',
    )
    def __str__(self):
        return self.name


class SmallDistrict (models.Model):
    # 신수동
    name = models.CharField(
        max_length=15, verbose_name="동읍리",
    )
    big_district = models.ForeignKey(
        BigDistrict,
        on_delete=models.CASCADE,
        related_name='small_districts'
    )

    def __str__(self):
        return self.big_district.name + ' ' + self.name


class Academy(models.Model):
    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        verbose_name='종목', related_name='academies',
    )
    name = models.CharField(max_length=255, verbose_name='업체명')
    profile_image = models.ImageField(
        default=None, null=True, blank=True,
    )
    introduction = models.TextField(
        blank=True, null=True, verbose_name='업체 소개',
    )
    phone = models.CharField(
        max_length=31, verbose_name='업체 문의번호',
    )
    email = models.EmailField(
        blank=True, null=True, verbose_name='업체 이메일',
    )
    operation_time = models.CharField(
        default='업체에 문의해주세요!', max_length=255,
        verbose_name='업체 운영 시간',
    )
    sns = models.URLField(null=True, blank=True, default=None)
    website = models.URLField(null=True, blank=True, default=None)
    small_district = models.ForeignKey(
        SmallDistrict,
        on_delete=models.CASCADE,
        related_name='locations',
        default=1,
        verbose_name='행정동'
    )
    # 중앙로 23길 3층 서강클라이밍
    address = models.CharField(
        max_length=255, default='업체에 문의해주세요!',
        verbose_name='업체 세부 주소',
    )

    lati = models.FloatField(default=0)
    long = models.FloatField(default=0)

    class Meta:
        verbose_name = '업체'
        verbose_name_plural = '업체'

    def __str__(self):
        return "["+str(self.sport.name)+"] "+str(self.name)


class Coach(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='코치 이름',
    )
    academy = models.ForeignKey(
        Academy, on_delete=models.CASCADE,
        verbose_name='소속 업체', related_name='coaches',
    )
    introduction = models.TextField(
        blank=True, null=True, verbose_name='코치 소개',
    )
    phone = models.CharField(
        max_length=255, verbose_name='코치 번호',
        default='업체에 문의해주세요!',
    )
    email = models.EmailField(verbose_name='코치 이메일', default=None, blank=True, null=True,)

    class Meta:
        verbose_name = '코치'
        verbose_name_plural = '코치'

    def __str__(self):
        return '['+str(self.academy.name)+'] '+str(self.name)


class Lesson(models.Model):
    academy = models.ForeignKey(
        Academy,
        null=True,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    title = models.CharField(max_length=255, verbose_name='수업 이름')
    org_price = models.PositiveSmallIntegerField(verbose_name='정가', default=0)
    dc_price = models.PositiveSmallIntegerField(verbose_name='할인가', null=True, blank=True, default=0)
    lesson_time = models.CharField(
        default='코치에게 문의해주세요!',
        max_length=255, verbose_name='수업 시간',
    )
    lesson_days = models.CharField(
        default='코치에게 문의해주세요!',
        max_length=255, verbose_name='수업 요일',
    )
    week_frequency = models.IntegerField(verbose_name='주간 횟수')
    coach = models.ForeignKey(
        Coach,
        null=True,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    introduction = models.CharField(max_length=127, default='   ')
    description = models.TextField(null=True, blank=True)
    LESSON_TYPE_CHOICES = (
        ('ONE_DAY', '원데이 레슨'),
        ('ONE_POINT', '원포인트 레슨'),
        ('SHORT_TERM', '단기간 레슨'),
        ('LONG_TERM', '장기간 레슨'),
        ('ONE_TO_ONE', '1:1 레슨'),
        ('SMALL_GROUP', '소규모 그룹 레슨'),
        ('LARGE_GROUP', '대규모 그룹 레슨'),
    )
    lesson_type = models.CharField(
        choices=LESSON_TYPE_CHOICES,
        default='ONE_DAY',
        max_length=127,
    )
    rating = models.FloatField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    likes_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '레슨'
        verbose_name_plural = '레슨'

    def __str__(self):
        return '['+str(self.academy.name)+'] ' + str(self.title)

    @register.filter(name='update_like_counter')
    def update_like_count(self, delta):
        self.likes_count += delta
        self.save()


class LessonImage(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
    )
    image = models.ImageField()


class Review(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
    )
    written_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    rating = models.IntegerField()
    comment = models.CharField(max_length=255)


class Like (models.Model):
    liked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='likes',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE, related_name='likes',
    )
