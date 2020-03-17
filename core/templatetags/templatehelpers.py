from django import template
from core import models

register = template.Library()


@register.filter(name='times')
def times(number):
    rating = int(number)
    return range(rating)


@register.filter(name='int_make')
def int_make(number):
    num = int(number)
    return num


@register.filter(name='sport_active')
def sport_active(number, clicked_sport):
    region_list = list(map(int, clicked_sport))
    if number in region_list:
        return number
    else:
        return False


@register.filter(name='district_active')
def district_active(number, clicked_region):
    region_list = list(map(int, clicked_region))
    if number in region_list:
        return number
    else:
        return False


@register.filter(name='type_active')
def type_active(number, clicked_type):
    region_list = list(map(int, clicked_type))
    if number in region_list:
        return number
    else:
        return False


@register.filter(name='frequency_active')
def frequency_active(number, week_frequency):
    region_list = list(map(int, week_frequency))
    if number in region_list:
        return number
    else:
        return False


@register.filter(name='filter_active')
def filter_active(number, clicked_order):
    region_list = list(map(int, clicked_order))
    if number in region_list:
        return number
    else:
        return False


@register.filter(name='clicked_sports')
def clicked_sports(number):
    try:
        sport = models.Sport.objects.get(id=int(number)).name
        return sport
    except:
        return None


@register.filter(name='sports_id')
def sports_id(number):
    try:
        sport = models.Sport.objects.get(id=int(number)).id
        return sport
    except:
        return None


@register.filter(name='clicked_region')
def clicked_region(number):
    try:
        region = models.SmallDistrict.objects.get(id=int(number)).name
        return region
    except:
        return None


@register.filter(name='region_id')
def region_id(number):
    try:
        region = models.SmallDistrict.objects.get(id=int(number)).id
        return region
    except:
        return None


@register.filter(name='clicked_type')
def clicked_type(number):
    try:
        type = models.LessonType.objects.get(id=int(number)).name
        return type
    except:
        return None


@register.filter(name='type_id')
def type_id(number):
    try:
        type = models.LessonType.objects.get(id=int(number)).id
        return type
    except:
        return None


@register.filter(name='clicked_week_frequency')
def clicked_week_frequency(number):
    try:
        frequency = models.LessonWeekFrequency.objects.get(freq=int(number)).displayed_as
        return frequency
    except:
        return None


@register.filter(name='frequency_id')
def frequency_id(number):
    try:
        frequency = models.LessonWeekFrequency.objects.get(freq=int(number)).id
        return frequency
    except:
        return None


@register.filter(name='rate_round')
def rate_round(number):
    try:
        rounded = round(number, 2)
        return rounded
    except:
        return None