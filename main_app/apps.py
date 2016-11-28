from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MainAppConfig(AppConfig):
    name = 'main_app'
    verbose_name = _('MainApp|name')
