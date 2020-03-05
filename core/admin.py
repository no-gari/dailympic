from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Sport)
admin.site.register(BigDistrict)
admin.site.register(SmallDistrict)
admin.site.register(Academy)
admin.site.register(Coach)
admin.site.register(LessonType)
admin.site.register(LessonWeekFrequency)
admin.site.register(Lesson)
admin.site.register(LessonImage)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(WrongInfo)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'sex',]
