from django.shortcuts import redirect
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django_summernote.widgets import SummernoteWidget
from django.views import generic
from django.db import transaction
from django_filters.views import FilterView
import re
from . import filters
from . import models


def get_ipaddress(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for
    else:
        return request.META.get('REMOTE_ADDR')


# Create your views here.
class BoardListView(FilterView):
    filterset_class = filters.BoardListFilter
    template_name = 'board/user/board_list.html'
    paginate_by = 10

    def get_queryset(self):
        return models.Documents.objects.filter(board__mid=self.kwargs['mid'], is_notice=False).order_by('-id')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        max_index = len(paginator.page_range)

        index = page_obj.number

        #
        # pagination 표시를 위한 계산
        #
        half_window_size = 3
        # start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        # end_index = start_index + page_numbers_range
        start_index = index - half_window_size - 1 if index >= half_window_size + 1 else 0
        end_index = index + half_window_size if index <= max_index - half_window_size else max_index

        page_obj.page_range = paginator.page_range[start_index:end_index]

        context['page_obj'] = page_obj

        # 공지글만 따로 뽑아옴
        context['notice_list'] = models.Documents.objects.filter(board__mid=self.kwargs['mid'],
                                                                 is_notice=True).order_by('created_at')

        # mid
        mid = self.kwargs.get('mid', '')
        if mid != '' and mid != 'favicon.ico':
            context['mid'] = mid

        return context


class BoardDetailView(generic.DetailView):
    model = models.Documents
    template_name = 'board/user/board_detail.html'

    def get(self, request, *args, **kwargs):
        document_id = kwargs['pk']

        try:
            document = models.Documents.objects.get(id=document_id)
        except:
            messages.error(request, '잘못된 접근입니다. 관리자에게 문의해주세요.')
            return redirect(request.META['HTTP_REFERER'])
        # 이페이지를 보면 조회수를 증가
        document.readed_count += 1
        document.save()

        context = super().get(request, *args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 댓글 뽑아오기
        comment_list = models.Comments.objects.filter(document=self.object).order_by('created_at')
        #
        # pagination 표시를 위한 계산
        #
        paginator = Paginator(comment_list, 30)
        page_obj = paginator.page(self.request.GET.get('page', 1))
        max_index = len(paginator.page_range)
        index = page_obj.number
        half_window_size = 3
        start_index = index - half_window_size - 1 if index >= half_window_size + 1 else 0
        end_index = index + half_window_size if index <= max_index - half_window_size else max_index
        page_obj.page_range = paginator.page_range[start_index:end_index]

        context['is_paginated'] = True
        context['page_obj'] = page_obj

        return_url = self.request.GET.get('return_url', '')
        if return_url == '':
            return_url = reverse('board:board_list', kwargs={'mid': self.object.board.mid})
        context['return_url'] = return_url

        return context


class DocumentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget = SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '600px'}})
        self.mid = kwargs['initial'].get('mid')

    def clean(self):
        # 스팸키워드 적용
        board = models.Board.objects.get(mid=self.mid)
        title = self.cleaned_data['title']
        content = self.cleaned_data['content']

        title_is_ban = False
        content_is_ban = False
        if board.denied_word == True:
            word_list = models.DeniedWord.objects.all()
            for word_obj in word_list:
                regex = re.compile(word_obj.word)
                title_ban = regex.search(title)
                if title_ban != None:
                    word_obj.hit += 1
                    word_obj.save()
                    title_is_ban = True
                    continue

                content_ban = regex.search(content)
                if content_ban != None:
                    word_obj.hit += 1
                    word_obj.save()
                    content_is_ban = True
                    continue

        if title_is_ban == True:
            self.add_error('title', '금지어가 포함되어있습니다.')
        if content_is_ban == True:
            self.add_error('content', '금지어가 포함되어있습니다.')

        if title_is_ban == True or content_is_ban == True:
            raise forms.ValidationError(['금지어가 포함되어있습니다.'])

    class Meta:
        model = models.Documents
        fields = ('title', 'content', 'is_notice', 'is_secret', 'comment_is_secret',)


class DocumentCreateView(generic.CreateView):
    model = models.Documents
    form_class = DocumentCreateForm
    template_name = 'board/user/document_add.html'

    def get_initial(self):
        return {'mid': self.kwargs.get('mid')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mid = self.kwargs.get('mid')
        context['board_obj'] = models.Board.objects.get(mid=mid)
        return context

    def dispatch(self, request, *args, **kwargs):
        mid = kwargs.get('mid')
        if not request.user.is_superuser:
            messages.error(request, '작성 권한이 없는 게시판입니다.')
            return HttpResponseRedirect(reverse('board:board_list', kwargs={'mid': mid}))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        mid = self.kwargs.get('mid')
        board = models.Board.objects.get(mid=mid)

        transaction.set_autocommit(False)
        try:
            form.instance.board = board
            form.instance.user = self.request.user
            form.instance.ipaddress = get_ipaddress(self.request)

            object = super().form_valid(form)

            content = self.request.POST['content']
            img_contents = re.findall(r'django-summernote/.*?"', content)
            for img in img_contents:
                imgs_path = img[0:len(img) - 1]
                summernote = models.Summernote.objects.get(file=imgs_path)
                summernote.document = form.instance
                summernote.save()

            # 첨부파일 등록
            files = self.request.FILES.getlist('input2')
            for f in files:
                file_instance = models.Files(document=form.instance, file=f, org_file_name=f.name)
                file_instance.save()

            transaction.commit()
            messages.success(self.request, '게시글이 등록되었습니다.')
        except:
            transaction.rollback()
            object = super().form_invalid(form)
            messages.error(self.request, '게시글을 등록하지 못했습니다.')

        return object

    def get_success_url(self):
        return reverse('board:board_list', kwargs={'mid': self.kwargs.get('mid')})


class DocumentUpdateView(generic.UpdateView):
    model = models.Documents
    form_class = DocumentCreateForm
    template_name = 'board/user/document_add.html'

    def get_initial(self):
        document_id = self.kwargs.get('pk', 0)
        mid = models.Documents.objects.get(id=document_id).board.mid
        return {'mid': mid}

    def dispatch(self, request, *args, **kwargs):
        document_id = self.kwargs.get('pk', 0)
        document = models.Documents.objects.get(id=document_id)
        if not request.user.is_superuser:
            if document.user != request.user:
                messages.error(request, '수정 불가능합니다.')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_id = self.kwargs.get('pk', 0)
        context['board_obj'] = models.Documents.objects.get(id=document_id).board

        # 첨부파일
        context['files_obj'] = models.Files.objects.filter(document_id=document_id)
        return context

    def form_valid(self, form):
        transaction.set_autocommit(False)
        try:
            form.instance.ipaddress = get_ipaddress(self.request)

            object = super().form_valid(form)

            content = self.request.POST['content']
            img_contents = re.findall(r'django-summernote/.*?"', content)
            for img in img_contents:
                imgs_path = img[0:len(img) - 1]
                summernotes = models.Summernote.objects.filter(file=imgs_path)
                if summernotes.exists():
                    summernote = summernotes.first()
                    summernote.document = form.instance
                    summernote.save()

            # 첨부파일 등록
            files = self.request.FILES.getlist('input2')
            for f in files:
                file_instance = models.Files(document=form.instance, file=f, org_file_name=f.name)
                file_instance.save()

            transaction.commit()
            messages.success(self.request, '게시글이 수정되었습니다.')
        except:
            transaction.rollback()
            object = super().form_invalid(form)
            messages.error(self.request, '게시글을 수정하지 못했습니다.')

        return object

    def get_success_url(self):
        return reverse('board:board_detail', kwargs={'pk': self.object.id}) + '?' + self.request.GET.get('return_url')


class DocumentDeleteView(generic.View):
    model = models.Documents
    template_name = 'board/user/document_add.html'

    def get_initial(self):
        document_id = self.kwargs.get('pk', 0)
        mid = models.Documents.objects.get(id=document_id).board.mid
        return {'mid': mid}


    def dispatch(self, request, *args, **kwargs):
        document_id = self.kwargs.get('pk', 0)
        document = models.Documents.objects.get(id=document_id)
        if not request.user.is_superuser:
            messages.error(request, '삭제 불가능합니다.')
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        document_id = kwargs.get('pk', 0)
        document = models.Documents.objects.get(id=document_id)

        document.delete()
        return HttpResponseRedirect(self.request.GET.get('return_url'))

def file_download(request, pk):
    file = models.Files.objects.get(id=pk)
    response = FileResponse(file.file, as_attachment=True, filename=file.org_file_name)
    return response


def set_file_delete(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'false',
            'message': '권한이 없습니다.',
        })

    file_id = request.POST.get('file_id')
    file_obj = models.Files.objects.get(id=file_id)

    if not request.user.is_staff:
        if file_obj.document.user != request.user:
            return JsonResponse({
                'status': 'false',
                'message': '권한이 없습니다.',
            })

    file_obj.delete()

    return JsonResponse({
        'status': 'true',
        'message': '첨부파일을 삭제하였습니다.',
    })


from django import VERSION as django_version
from django_summernote.utils import get_attachment_model, using_config
from django.template.loader import render_to_string


@using_config
def upload_attachment(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'false',
            'message': _('Only POST method is allowed'),
        }, status=400)

    authenticated = \
        request.user.is_authenticated if django_version >= (1, 10) \
            else request.user.is_authenticated()

    if config['attachment_require_authentication'] and \
            not authenticated:
        return JsonResponse({
            'status': 'false',
            'message': _('Only authenticated users are allowed'),
        }, status=403)

    if not request.FILES.getlist('files'):
        return JsonResponse({
            'status': 'false',
            'message': _('No files were requested'),
        }, status=400)

    # remove unnecessary CSRF token, if found
    kwargs = request.POST.copy()
    kwargs.pop("csrfmiddlewaretoken", None)

    try:
        attachments = []

        for file in request.FILES.getlist('files'):

            # create instance of appropriate attachment class
            klass = get_attachment_model()
            attachment = klass()

            attachment.file = file
            attachment.name = file.name
            attachment.user = request.user
            attachment.ipaddress = get_ipaddress(request)

            if file.size > config['attachment_filesize_limit']:
                return JsonResponse({
                    'status': 'false',
                    'message': _('File size exceeds the limit allowed and cannot be saved'),
                }, status=400)

            # calling save method with attachment parameters as kwargs
            attachment.save(**kwargs)
            attachments.append(attachment)

        return HttpResponse(render_to_string('django_summernote/upload_attachment.json', {
            'attachments': attachments,
        }), content_type='application/json')
    except IOError:
        return JsonResponse({
            'status': 'false',
            'message': _('Failed to save attachment'),
        }, status=500)
