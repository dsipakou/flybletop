from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms.utils import ErrorList

from Flybletop import settings


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
        u = User.objects.create_user(data['username'],
                                 data['email'],
                                 data['password1'])
        u.is_active = False
        u.save()
        return u

    def sendEmail(self, data):
        link = '{0}/activate/{1}'.format(settings.BASE_DIR, data['activation_key'])
        send_mail(data['email_subject'], 'test message', 'mail@mail.te', [('mc.flyer@gmail.com')], fail_silently=False)
