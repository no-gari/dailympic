from django import template
from django.shortcuts import render
from django.utils.safestring import mark_safe
import string
import random
from board import models

register = template.Library()

@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url

@register.filter
def get_inputtype(field, str):
    template_name = field.subwidgets[0].template_name
    if str in template_name:
        return True
    else:
        return False
    

@register.simple_tag
def get_board_widget(request, mid, order, limit, format, user_YN, link_target, title_bold, add_css1='', add_css2='', add_css3=''):
    if order == 'asc':
        orderby = 'id'
    else:
        orderby = '-id'

    limit = int(limit)
    string_pool = string.ascii_letters
    uuid = []
    for i in range(20):
        uuid += random.choices(string_pool)
    
    if link_target == '_blank':
        link_target = '_blank'
    else:
        link_target = '_self'
    
    board_obj = models.Documents.objects.filter(board__mid=mid).order_by(orderby)[:limit]
    render_data = render(request, 'board/user/board_widget.html', {
        'board_obj': board_obj,
        'format': format,
        'user_YN': user_YN,
        'uuid': ''.join(uuid),
        'link_target': link_target,
        'add_css1': add_css1,
        'add_css2': add_css2,
        'add_css3': add_css3,
        'title_bold': title_bold
    })
    return mark_safe(render_data.content.decode('utf-8'))