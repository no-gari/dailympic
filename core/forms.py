from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label='아이디')
    password = forms.CharField(label='비밀번호')
    password2 = forms.CharField(label='비밀번호 확인')
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)


# class UserForm(UserCreationForm):
#     error_messages = {
#         'password_mismatch': '잘못된 비밀번호입니다.',
#     }
#     first_name = forms.CharField()
#     last_name = forms.CharField()
#     email = forms.EmailField()
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if email is None:
#             raise forms.ValidationError('email input error')
#         return email
#
#     def clean_first_name(self):
#         name = self.cleaned_data.get('first_name')
#         if name is None:
#             raise forms.ValidationError('input  firstname')
#         return name
#
#     def clean_last_name(self):
#         name = self.cleaned_data.get('last_name')
#         if name is None:
#             raise forms.ValidationError('input last name')
#         return name
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
#         if commit:
#             user.save()
#         return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

