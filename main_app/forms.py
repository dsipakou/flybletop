from django import forms
from Flybletop import settings
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _

from main_app.models import Profile


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=50)


class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control'}), max_length=40, min_length=3)
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}), max_length=40, min_length=6)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'form-control'}), max_length=30, min_length=3)
    email = forms.EmailField(label="", widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': 'form-control'}), max_length=100,
                             error_messages={'invalid': "Invalid e-mail"})
    password1 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm a password',
                                                                  'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        if len(User.objects.filter(username=username)) > 0:
            self._errors['username'] = ErrorList(['Given username is already in use'])
        email = self.cleaned_data.get('email')
        if len(User.objects.filter(email=email)) > 0:
            self._errors['email'] = ErrorList(['Given email address is already in use'])
        password1 = self.cleaned_data.get('password1')

        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password1'] = ErrorList([''])
            self._errors['password2'] = ErrorList(['Passwords are not equal'])

        return self.cleaned_data

    def save(self, data):
        u = User.objects.create_user(data['username'], data['email'], data['password1'])
        u.save()
        profile = Profile()
        profile.user = u
        profile.save()
        return u


class RecoveryForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(
        attrs={'placeholder': 'Your E-mail', 'class': 'form-control'}), max_length=100,
                             error_messages={'invalid': "Invalid e-mail"})

    def clean(self):
        email = self.cleaned_data.get('email')
        if len(User.objects.filter(email=email)) == 0:
            self._errors['email'] = ErrorList([_('We have no such e-mail address in our database')])

        return self.cleaned_data

    def send_email(self, data):
        user = User.objects.filter(email=data['email'])[0]
        profile = Profile.objects.filter(user=user)[0]

        link = settings.BASE_DIR
