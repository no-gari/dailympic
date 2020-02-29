from django.db import models
from enum import Enum
from django.contrib.auth.models import User, Group, UserManager
from django_summernote import models as summermodel
from django_summernote.utils import get_attachment_storage, get_attachment_upload_to
from simple_history.models import HistoricalRecords
import os
from functools import partial
import uuid

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class Board(models.Model):
    class Grant(ChoiceEnum):
        all = '모든 사용자'
        join = '가입한 사용자'
        super = '관리자만'
        group = '선택 그룹 사용자'
    
    board_title = models.CharField(max_length=255, verbose_name='게시판 이름', help_text='게시판 이름을 입력합니다.')
    mid = models.CharField(unique=True, max_length=255, verbose_name='게시판 고유값', help_text='영문+숫자 조합만 가능하며 게시판 주소값입니다. 접근방법예시(127.0.0.1/board/<고유값>)')
    board_description = models.TextField(blank=True, null=True, verbose_name='게시판 설명', help_text='게시판에 대한 간단한 설명을 입력합니다.')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    board_grant = models.CharField(max_length=6, default='all', choices=Grant.choices(), verbose_name='권한 설정', help_text='권한을 설정합니다. 선택그룹사용자 일경우 그룹 권한에 기반합니다.')
    user = models.ManyToManyField(User, through='UserGrant', verbose_name='유저 권한', help_text='유저권한을 부여하면 권한 설정,그룹 권한에 관계없이 최상위 권한으로 동작합니다.')
    denied_word = models.BooleanField(default=True, verbose_name='스팸 키워드', help_text='해당부분을 체크하면 스팸 키워드필터가 적용됩니다.')
    
    def __str__(self):
        return str(self.board_title)
    
    class Meta:
        verbose_name = '게시판'
        verbose_name_plural = '게시판'
    
    
class UserGrant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='유저 권한')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='게시판')
    grant_list = models.BooleanField(default=False, verbose_name='목록')
    grant_view = models.BooleanField(default=False, verbose_name='글열람')
    grant_write_document = models.BooleanField(default=False, verbose_name='글 작성')
    grant_write_comment = models.BooleanField(default=False, verbose_name='댓글 작성')
    grant_super = models.BooleanField(default=False, verbose_name='관리자', help_text='체크시 모든글에대한 슈퍼유저권한을 가집니다.')
    
    def __str__(self):
        return str(self.user) + '의 유저권한'
    
    class Meta:
        unique_together = ('user', 'board',)
        verbose_name = '유저 권한'
        verbose_name_plural = '유저 권한을 부여하면 권한 설정, 그룹 권한에 관계없이 최상위 권한으로 동작합니다.'
        
        
class Documents(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='게시판')
    is_notice = models.BooleanField(default=False, verbose_name='공지')
    title = models.CharField(max_length=255, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    readed_count = models.PositiveIntegerField(default=0, verbose_name='조회수')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='글쓴이')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    ipaddress = models.GenericIPAddressField()
    is_secret = models.BooleanField(default=False, verbose_name='글 비공개')
    comment_is_secret = models.BooleanField(default=False, verbose_name='댓글 비공개')
    history = HistoricalRecords()

    def __str__(self):
        return str(self.board.board_title) + ' - ' + str(self.title)

    class Meta:
        verbose_name = '문서'
        verbose_name_plural = '문서'
    
    
class Comments(models.Model):
    document = models.ForeignKey(Documents, on_delete=models.CASCADE, verbose_name='문서')
    is_secret = models.BooleanField(default=False, verbose_name='댓글 비공개')
    content = models.TextField(verbose_name='내용')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='글쓴이')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    ipaddress = models.GenericIPAddressField()
    
    def __str__(self):
        return str(self.document.board.board_title) + ' - ' + str(self.document.title) + ' 의 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
        
        
def _update_filename(instance, filename, path):

    from datetime import datetime
    today = datetime.now()
    path = path.replace('%Y', today.strftime('%Y'))
    path = path.replace('%m', today.strftime('%m'))
    path = path.replace('%d', today.strftime('%d'))

    file_ext = filename.split('.')
    file_ext = file_ext[len(file_ext) - 1]

    filename = "{}.{}".format(uuid.uuid4(),file_ext)

    return os.path.join(path, filename)

def upload_to(path):
    return partial(_update_filename, path=path)
    
class Files(models.Model):
    document = models.ForeignKey(Documents, on_delete=models.CASCADE, verbose_name='문서')
    file = models.FileField(upload_to=upload_to('file/%Y/%m/%d/'), verbose_name='첨부 자료')
    org_file_name = models.CharField(max_length=255, blank=True, verbose_name='원본파일명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    def __str__(self):
        return str(self.document.title) + ' 의 첨부 파일'

    class Meta:
        verbose_name = '첨부 파일'
        verbose_name_plural = '첨부 파일'
        
        
class Summernote(summermodel.AbstractAttachment):
    document = summermodel.models.ForeignKey(Documents, null=True, blank=True, verbose_name='문서', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='원본파일명', help_text="Defaults to filename, if left blank")
    file = models.FileField(
        upload_to=get_attachment_upload_to(),
        storage=get_attachment_storage(),
        unique=True
    )
    ipaddress = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='글쓴이')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '첨부 이미지'
        verbose_name_plural = '첨부 이미지'


class BoardGroupGrant(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='그룹')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='게시판')
    grant_list = models.BooleanField(default=False, verbose_name='목록')
    grant_view = models.BooleanField(default=False, verbose_name='글열람')
    grant_write_document = models.BooleanField(default=False, verbose_name='글 작성')
    grant_write_comment = models.BooleanField(default=False, verbose_name='댓글 작성')
    grant_super = models.BooleanField(default=False, verbose_name='관리자', help_text='체크시 해당그룹은 모든글에대한 슈퍼유저권한을 가집니다.')
    
    def __str__(self):
        return str(self.group.name) + '의 그룹권한'
    
    class Meta:
        unique_together = ('board', 'group',)
        verbose_name = '그룹 권한'
        verbose_name_plural = '권한설정에서 선택 그룹 사용자 일때 동작합니다.'
        

class DeniedWord(models.Model):
    word = models.CharField(max_length=255, verbose_name='키워드', help_text='키워드를 입력하세요.')
    hit = models.IntegerField(default=0, verbose_name='스팸횟수')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    def __str__(self):
        return '스팸 키워드 - ' + str(self.word)
    
    class Meta:
        verbose_name = '스팸 키워드'
        verbose_name_plural = '스팸 키워드'