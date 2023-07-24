from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BdanswersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bdanswers'
    verbose_name = _('Ответы на билеты по базам данных')
