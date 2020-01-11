from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = '핵심 기능'


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'

    menu = (
        ParentItem('조직 관리', children=[
            ChildItem(model='auth.user'),
            ChildItem(model='auth.group'),
        ], icon='fa fa-users'),
        ParentItem('종목 관리', children=[
            ChildItem(model='core.sport'),
        ], icon='fa fa-users'),
        ParentItem('업체 관리', children=[
            ChildItem(model='core.academy'),
        ], icon='fa fa-users'),
        ParentItem('코치 관리', children=[
            ChildItem(model='core.coach'),
        ], icon='fa fa-users'),
        ParentItem('레슨 관리', children=[
            ChildItem(model='core.lesson'),
        ], icon='fa fa-users'),
        ParentItem('위치 관리', children=[
            ChildItem(model='core.district'),
            ChildItem(model='core.location'),
        ], icon='fa fa-leaf'),
        ParentItem('board_manage', children=[
            ChildItem(model='board.board'),
            ChildItem(model='board.documents'),
            ChildItem(model='board.comments'),
            ChildItem(model='board.files'),
            ChildItem(model='board.summernote'),
            ChildItem(model='board.deniedword'),
        ], icon='fa fa-users'),
    )