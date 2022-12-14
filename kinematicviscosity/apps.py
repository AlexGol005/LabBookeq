"""
Модуль проекта LabJournal, приложения kinematicviscosity.
Приложение kinematicviscosity это журнал фиксации
лабораторных записей по измерению кинематической вязкости нефтепродуктов
(Лабортаорный журнал измерения кинематической вязкости).

Данный модуль apps.py выводит раздел приложения в административной части сайта.
"""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ViscosityattestationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kinematicviscosity'

    verbose_name = _("Журнал измерения кинематической вязкости")
