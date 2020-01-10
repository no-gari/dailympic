from django.db import models
from django.contrib.auth.models import User, Group, UserManager


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
    description = models.TextField()
    LESSON_TYPE_CHOICES = (
        ('DAILY', '일일 레슨'),
        ('ONE_POINT', '원포인트 레슨'),
    )
    lesson_type = models.CharField(choices=LESSON_TYPE_CHOICES, max_length=127)
    rating = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    instagram = models.URLField(null=True, blank=True)
    navercafe = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = '레슨'
        verbose_name_plural = '레슨'

    def __str__(self):
        return str(self.academy.name) + '의 ' + str(self.title)


class LessonImage(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    image = models.ImageField()


class Review(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    written_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()


class District (models.Model):
    # 서울시 마포구 신수동
    name = models.CharField(max_length=20, verbose_name='지역')


class Location (models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='locations')
    lati = models.FloatField()
    long = models.FloatField()
    # 중앙로 23길 3층 서강클라이밍
    address = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, null=True, on_delete=models.SET_NULL, blank=True)

