from django import template
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


register = template.Library()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="유저",
    )
    image = models.ImageField(
        default=None,null=True,blank=True,verbose_name='프로필 사진',
        upload_to='profile/%Y/%m/%d',
    )
    name = models.CharField(max_length=31, verbose_name='이름')
    SEX_CHOICES = (
        ('M', '남'),
        ('W', '여')
    )
    sex = models.CharField(max_length=7, choices=SEX_CHOICES, verbose_name='성별', default='W')
    birthday = models.DateField(verbose_name='생년월일')
    phone = models.CharField(
        max_length=31,
        verbose_name='휴대전화',
        default='등록된 전화번호가 없습니다.'
    )

    def __str__(self):
        return self.user.username+'의 프로필'

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = '프로필'


class Sport(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='종목명',
    )
    icon = models.ImageField(
        default=None, null=True, blank=True,
        upload_to='sports/',
        verbose_name='종목 아이콘',
    )

    class Meta:
        verbose_name = '종목'
        verbose_name_plural = '종목'

    def __str__(self):
        return self.name


class BigDistrict (models.Model):
    # 서울시 마포구
    name = models.CharField(
        max_length=31, verbose_name='시군구',
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '시군구'
        verbose_name_plural = '시군구'


class SmallDistrict (models.Model):
    # 신수동
    name = models.CharField(
        max_length=15, verbose_name="동읍리",
    )
    big_district = models.ForeignKey(
        BigDistrict,
        on_delete=models.CASCADE,
        related_name='small_districts',
        verbose_name = "시군구",
    )

    def __str__(self):
        return self.big_district.name + ' ' + self.name

    class Meta:
        verbose_name = '동읍리'
        verbose_name_plural = '동읍리'


class Academy(models.Model):
    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        verbose_name='종목', related_name='academies',
    )
    name = models.CharField(max_length=255, verbose_name='업체명')
    profile_image = models.ImageField(
        default=None, null=True, blank=True,
        upload_to='academy/%Y/%m/%d',
        verbose_name='업체 프로필 이미지',
    )
    introduction = models.TextField(
        blank=True, null=True, verbose_name='업체 소개',
    )
    phone = models.CharField(
        max_length=31, verbose_name='업체 문의번호', default='-1'
    )
    email = models.EmailField(
        blank=True, null=True, verbose_name='업체 이메일', default='-1'
    )
    operation_time = models.TextField(
        default='업체에 문의해주세요!', max_length=255,
        verbose_name='업체 운영 시간',
        help_text='엔터로 구분해주세요. (ex)월,목 - 17:00 ~ 20:00 (enter키) 금 - 18:00 ~ 20:00'
    )
    instagram = models.URLField(default='-1',
                                verbose_name='인스타그램 링크')
    facebook = models.URLField(default='-1',
                               verbose_name='페이스북 링크')
    website = models.URLField(default='-1',
                              verbose_name='웹사이트/카페 링크')
    small_district = models.ForeignKey(
        SmallDistrict,
        on_delete=models.CASCADE,
        related_name='locations',
        default=1,
        verbose_name='업체 위치 행정동'
    )
    # 중앙로 23길 3층 서강클라이밍
    address = models.CharField(
        max_length=255, default='업체에 문의해주세요!',
        verbose_name='업체 세부 주소',
    )

    lati = models.FloatField(default=0, verbose_name='위도')
    long = models.FloatField(default=0, verbose_name='경도')

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
    career = models.TextField(
        verbose_name= '코치 커리어',
        help_text= '경력을 엔터로 구분해주세요',
        null=True,
        blank=True
    )
    introduction = models.TextField(
        blank=True, null=True, verbose_name='코치 짧은 소개',
    )
    phone = models.CharField(
        max_length=255, verbose_name='코치 번호',
        default='-1',
    )
    email = models.EmailField(
        verbose_name='코치 이메일', default='-1', blank=True, null=True,
    )
    instagram = models.URLField(
        null=True, blank=True, default='-1',
        verbose_name='코치 인스타그램 링크'
    )
    facebook = models.URLField(
        null=True, blank=True, default='-1',
        verbose_name='코치 페이스북 링크'
    )
    image = models.ImageField(
        verbose_name='코치 사진',
        null=True, blank=True, upload_to='coach/%Y/%m/%d'
    )

    class Meta:
        verbose_name = '코치'
        verbose_name_plural = '코치'

    def __str__(self):
        return '['+str(self.academy.name)+'] '+str(self.name)


class LessonType(models.Model):
    name = models.CharField(
        max_length=127,
        verbose_name='레슨 유형',
    )
    CLASSIFED_CHOICE_SET = (
        ('RECRUIT', 'RECRUIT'),
        ('METHOD', 'METHOD')

    )
    classified_as = models.CharField(
        max_length=127,
        verbose_name='대분류',
        default='METHOD',
        choices=CLASSIFED_CHOICE_SET,
    )

    class Meta:
        verbose_name = '레슨 유형'
        verbose_name_plural = '레슨 유형'

    def __str__(self):
        return '(' + str(self.pk) + ')' + str(self.name)


class LessonWeekFrequency(models.Model):
    freq = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name='주 레슨 횟수'
    )
    displayed_as = models.CharField(
        verbose_name='표시 이름',
        max_length=31,
    )

    class Meta:
        verbose_name = '레슨 횟수'
        verbose_name_plural = '레슨 횟수'

    def __str__(self):
        return self.displayed_as


class Lesson(models.Model):
    academy = models.ForeignKey(
        Academy,
        null=True,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='소속 업체'
    )
    title = models.CharField(max_length=255, verbose_name='레슨 이름')
    org_price = models.PositiveIntegerField(
        verbose_name='정가', default=0
    )
    dc_price = models.PositiveIntegerField(
        verbose_name='할인가', null=True, blank=True
    )
    lesson_time = models.TextField(
        default='코치에게 문의해주세요!',
        max_length=255, verbose_name='레슨 시간',
        help_text='엔터로 구분해주세요. (ex)월,목 - 17:00 ~ 20:00 (enter키) 금 - 18:00 ~ 20:00'
    )
    week_frequency = models.ManyToManyField(
        LessonWeekFrequency,
        related_name='lessons',
        related_query_name='week_frequencies',
        verbose_name='주간 횟수',
    )
    coach = models.ManyToManyField(
        Coach,
        related_name='lessons',
        related_query_name='coaches',
        verbose_name='코치'
    )
    introduction = models.CharField(
        max_length=127, default='  ',
        verbose_name="레슨 짧은 소개",
        help_text='레슨 리스트에서 보여지는 짧은 문구입니다'
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name='레슨 상세 설명'
    )
    # LESSON_TYPE_CHOICES = (
    #     ('ONE_DAY', '원데이 레슨'),
    #     ('ONE_POINT', '원포인트 레슨'),
    #     ('SHORT_TERM', '단기간 레슨'),
    #     ('LONG_TERM', '장기간 레슨'),
    #     ('ONE_TO_ONE', '1:1 레슨'),
    #     ('SMALL_GROUP', '소규모 그룹 레슨'),
    #     ('LARGE_GROUP', '대규모 그룹 레슨'),
    # )
    lesson_type = models.ManyToManyField(
        LessonType,
        verbose_name='레슨 유형',
        related_name='lessons',
    )
    rating_total = models.BigIntegerField(
        default=0,
        verbose_name='레슨 평점 총합'
    )
    review_count = models.PositiveIntegerField(
        default=0,
        verbose_name='후기 개수'
    )
    rating = models.FloatField(
        default=0,
        verbose_name='레슨 평점'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='작성일자'
    )
    likes_count = models.PositiveIntegerField(
        default=0,
        verbose_name='찜한 유저 수'
    )

    class Meta:
        verbose_name = '레슨'
        verbose_name_plural = '레슨'

    def __str__(self):
        return '('+str(self.id)+')['+str(self.academy.name)+'] ' + str(self.title)


class LessonImage(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='레슨'
    )
    image = models.ImageField(
        upload_to='lesson/%Y/%m/%d',
        verbose_name='레슨 이미지'
    )

    class Meta:
        verbose_name = '레슨 이미지'
        verbose_name_plural = '레슨 이미지'


class Review(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='레슨'
    )
    written_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='작성자'
    )
    rating = models.IntegerField(
        verbose_name='레슨 평점'
    )
    comment = models.CharField(
        max_length=255, verbose_name='후기내용',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='작성시간',
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = '후기'
        verbose_name_plural = '후기'

    def __str__(self):
        return self.comment + '('+self.lesson.title+')'


class Like (models.Model):
    liked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE, related_name='likes',
        verbose_name='유저'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE, related_name='likes',
        verbose_name='레슨',
    )

    class Meta:
        verbose_name = '찜'
        verbose_name_plural = '찜'


class WrongInfo (models.Model):
    phone_num = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        verbose_name = '오류 신고'
        verbose_name_plural = '오류 신고'