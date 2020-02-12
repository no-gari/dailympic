from django import template
register = template.Library()

@register.filter(name='times')
def times(number):
    rating = int(number)
    return range(rating)