from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from django_summernote.admin import SummernoteModelAdmin
from simple_history.admin import SimpleHistoryAdmin
import re
from . import models
from . import views


class UserGrantInlineAdmin(admin.StackedInline):
    model = models.UserGrant
    autocomplete_fields = ['user']

class BoardGroupGrantInlineAdmin(admin.StackedInline):
    model = models.BoardGroupGrant
    autocomplete_fields = ['group']

class BoardAdminForm(forms.ModelForm):
    class Meta:
        model = models.Board
        fields = ('board_title', 'mid', 'board_description', 'board_grant', 'denied_word',)

    def clean(self):
        # mid 값 검증
        r = re.compile(r'[^A-Za-z0-9]+')
        result = r.search(self.cleaned_data['mid'])
        if result is not None:
            self.add_error('mid', '영문+숫자만 가능합니다.')
            raise forms.ValidationError([])

@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    form = BoardAdminForm
    list_display = ('get_id', 'board_title', 'mid', 'board_grant', 'created_at', 'updated_at',)
    list_display_links = ('board_title',)
    search_fields = ('board_title', 'mid',)
    inlines = (UserGrantInlineAdmin, BoardGroupGrantInlineAdmin,)
    
    def get_id(self, obj):
        return obj.id
    get_id.short_description = 'ID'


class FilesInlineAdmin(admin.StackedInline):
    model = models.Files
    readonly_fields = ['file_image_small']
    
    def file_image_small(self, obj):
        if obj.org_file_name != '':
            file_ext = obj.org_file_name.split('.')[1]
            if file_ext in ['jpg','jpeg','png','gif','bmp']:
                return mark_safe('<img src="{url}" height="100" />'.format(url=obj.file.url))
            else:
                return mark_safe('this is not image')
    file_image_small.short_description = '이미지'
    
    class Media:
        js = (
            'js/myscript.js',
        )


class DocumentsAdminForm(forms.ModelForm):
    class Meta:
        model = models.Documents
        fields = ('board', 'is_notice', 'title', 'content', 'readed_count', 'user', 'ipaddress', 'is_secret', 'comment_is_secret',)

    def save(self, commit=True):
        try:
            self.instance.user = self.request.user
            self.instance.ipaddress = views.get_ipaddress(self.request)
    
            instance = super().save(commit=False)
            instance.save()
            
            content = self.cleaned_data['content']
            img_contents = re.findall(r'django-summernote/.*?"', content)
            for img in img_contents:
                imgs_path = img[0:len(img) - 1]
                summernote = models.Summernote.objects.get(file=imgs_path)
                summernote.document = instance
                summernote.save()
        except:
            instance = super().save(commit=False)

        return instance



@admin.register(models.Documents)
class DocumentsAdmin(SummernoteModelAdmin, SimpleHistoryAdmin):
    form = DocumentsAdminForm
    list_display = ('get_id', 'board', 'title', 'is_notice', 'readed_count', 'user', 'created_at', 'updated_at', 'ipaddress', 'is_secret', 'comment_is_secret', 'show_document_url',)
    list_display_links = ('title',)
    list_filter = ['board__board_title', 'is_notice', 'is_secret', 'comment_is_secret']
    autocomplete_fields = ['board']
    search_fields = ('title', 'user',)
    readonly_fields = ('ipaddress', 'user',)
    summernote_fields = ('content',)
    inlines = (FilesInlineAdmin,)
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.request = request
        return form
    
    def get_id(self, obj):
        return obj.id
    get_id.short_description = 'ID'
    
    def show_document_url(self, obj):
        url = reverse('board:board_detail', kwargs={'pk': obj.id}) + '?return_url=' + reverse('board:board_list', kwargs={'mid': obj.board.mid})
        return format_html("<a href='{}' target='_blank'>문서로 이동</a>", url)
    show_document_url.short_description = "문서"
    
        

@admin.register(models.Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'content', 'is_secret', 'user', 'created_at', 'updated_at', 'ipaddress', 'show_comment_url',)
    list_display_links = ('content',)
    readonly_fields = ('ipaddress', 'user',)
    list_filter = ['document__board__board_title', 'is_secret']
    autocomplete_fields = ['document']
    
    def get_id(self, obj):
        return obj.id
    get_id.short_description = 'ID'

    def show_comment_url(self, obj):
        url = reverse('board:board_detail', kwargs={'pk': obj.document.board.id}) + '?return_url=' + reverse('board:board_list', kwargs={'mid': obj.document.board.mid}) + '#comment_{}'.format(obj.id)
        return format_html("<a href='{}' target='_blank'>댓글로 이동</a>", url)
    show_comment_url.short_description = "댓글"

    def save_model(self, request, obj, form, change):
        if obj.user_id is None:
            obj.user = request.user
        if obj.ipaddress is None:
            obj.ipaddress = views.get_ipaddress(request)
        return super().save_model(request, obj, form, change)
     
        
@admin.register(models.Files)
class FilesAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'document', 'file', 'org_file_name', 'created_at', 'updated_at',)
    list_display_links = ('document',)
    list_filter = ['document__board__board_title']
    search_fields = ('org_file_name',)
    readonly_fields = ['file_image_small']
    autocomplete_fields = ['document']
    
    def get_id(self, obj):
        return obj.id
    get_id.short_description = 'ID'
    
    def file_image_small(self, obj):
        if obj.org_file_name != '':
            file_ext = obj.org_file_name.split('.')[1]
            if file_ext in ['jpg','jpeg','png','gif','bmp']:
                return mark_safe('<img src="{url}" height="100" />'.format(url=obj.file.url))
            else:
                return mark_safe('this is not image')
    file_image_small.short_description = '이미지'


admin.site.unregister(models.Summernote)
@admin.register(models.Summernote)
class SummernoteAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'user', 'document', 'name', 'file', 'uploaded', 'ipaddress',)
    list_display_links = ('document', 'name',)
    readonly_fields = ['document', 'ipaddress','user', 'name', 'file_image_small']
    autocomplete_fields = ['document']
    
    def get_id(self, obj):
        return obj.id
    get_id.short_description = 'ID'

    def has_add_permission(self, request):
        return False

    def file_image_small(self, obj):
        if obj.name != '':
            file_ext = obj.name.split('.')[1]
            if file_ext in ['jpg','jpeg','png','gif','bmp']:
                return mark_safe('<img src="{url}" height="100" />'.format(url=obj.file.url))
            else:
                return mark_safe('this is not image')
    file_image_small.short_description = '이미지'


@admin.register(models.DeniedWord)
class DeniedWordAdmin(admin.ModelAdmin):
    list_display = ('get_id', 'word', 'hit', 'created_at',)
    list_display_links = ('word',)
    readonly_fields = ['hit', 'created_at']
    
    def get_id(self, obj):
        return obj.id
    get_id.short_description = 'ID'