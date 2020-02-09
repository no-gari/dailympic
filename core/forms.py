from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    error_messages = {
        'password_mismatch': '비밀번호가 일치하지 않습니다.',
    }
    username = forms.CharField(label='아이디')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError('email input error')
        return email

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
