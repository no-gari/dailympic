from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from django.contrib.auth.models import User

# class UserForm(forms.ModelForm):
#     username = forms.CharField(label='아이디')
#     password = forms.CharField(label='비밀번호')
#     password2 = forms.CharField(label='비밀번호 확인')
#     email = forms.EmailField(label='이메일')
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'email')
#
#     def save(self, commit=True):
#         """
#         Save this form's self.instance object if commit=True. Otherwise, add
#         a save_m2m() method to the form which can be called after the instance
#         is saved manually at a later time. Return the model instance.
#         """
#         if self.errors or self.password != self.password2:
#             raise ValueError(
#                 "The %s could not be %s because the data didn't validate." % (
#                     self.instance._meta.object_name,
#                     'created' if self.instance._state.adding else 'changed',
#                 )
#             )
#         if commit:
#             # If committing, save the instance and the m2m data immediately.
#             self.instance.save()
#             self._save_m2m()
#         else:
#             # If not committing, add a method to the form to allow deferred
#             # saving of m2m data.
#             self.save_m2m = self._save_m2m
#         return self.instance
#
#     save.alters_data = True


class UserForm(UserCreationForm):
    error_messages = {
        'password_mismatch': '비밀번호가 일치하지 않습니다.',
    }
    email = forms.EmailField()

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
