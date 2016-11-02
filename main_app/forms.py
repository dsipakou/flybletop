from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label='Поиск', max_length=50)


class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
