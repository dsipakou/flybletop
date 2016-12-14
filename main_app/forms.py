import datetime

from django import forms
from django.core.mail import send_mail
from django.utils import timezone

from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _

from Flybletop import settings
from main_app.models import Profile


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=50)


class ActivationForm(forms.Form):
    code = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': _('ActivationCode'), 'class': 'form-control'}), max_length=30, min_length=3)


class LoginForm(forms.Form):
    email = forms.EmailField(label="", widget=forms.EmailInput(
        attrs={'placeholder': _('Email'), 'class': 'form-control'}), max_length=100,
                             error_messages={'invalid': _('Invalid e-mail')})
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'), 'class': 'form-control'}), max_length=40, min_length=6)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': _('Username'), 'class': 'form-control'}), max_length=30, min_length=3)
    email = forms.EmailField(label="", widget=forms.EmailInput(
        attrs={'placeholder': _('Email'), 'class': 'form-control'}), max_length=100,
                             error_messages={'invalid': _('Invalid e-mail')})
    password1 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': _('Password'), 'class': 'form-control'}))
    password2 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': _('Confirm a password'),
                                                                  'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        if len(User.objects.filter(username=username)) > 0:
            self._errors['username'] = ErrorList([_('Given username is already in use')])
        email = self.cleaned_data.get('email')
        if len(User.objects.filter(email=email)) > 0:
            self._errors['email'] = ErrorList([_('Given email address is already in use')])
        password1 = self.cleaned_data.get('password1')

        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password1'] = ErrorList([''])
            self._errors['password2'] = ErrorList([_('Passwords are not equal')])

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
        attrs={'placeholder': _('Your E-mail'), 'class': 'form-control'}), max_length=100,
                             error_messages={'invalid': _('Invalid e-mail')})

    def clean(self):
        email = self.cleaned_data.get('email')
        if len(User.objects.filter(email=email)) == 0:
            self._errors['email'] = ErrorList([_('We have no such e-mail address in our database')])

        return self.cleaned_data

    def send_email(self, data):
        profile = Profile.objects.get(user__email=data['email'])
        profile.activation_key = data['activation_key']
        profile.key_expires = timezone.now() + datetime.timedelta(hours=6)
        profile.save()
        link = data['url'] + data['activation_key']
        send_mail(data['email_subject'], data['email_body'] + '\n\n' + link, settings.EMAIL_HOST_USER, [data['email']], fail_silently=False)


class NewPasswordForm(forms.Form):
    password1 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': _('Password'), 'class': 'form-control'}))
    password2 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm a password',
                                                                  'class': 'form-control'}))

    def clean(self):
        password1 = self.cleaned_data.get('password1')

        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password1'] = ErrorList([''])
            self._errors['password2'] = ErrorList([_('Passwords are not equal')])

        return self.cleaned_data

    def reset(self, data):
        user = User.objects.get(profile__activation_key=data['activation_key'])

        profile = Profile.objects.get(user=user)
        user.set_password(data['password1'])
        user.save()
        profile.activation_key = None
        profile.save()
