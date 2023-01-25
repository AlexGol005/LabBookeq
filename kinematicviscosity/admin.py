"""
Модуль проекта LabJournal, приложения kinematicviscosity.
Приложение kinematicviscosity это журнал фиксации
лабораторных записей по измерению кинематической вязкости нефтепродуктов
(Лабортаорный журнал измерения кинематической вязкости).

Данный модуль admin.py выводит таблицы приложения в административной части сайта.
"""

from django.contrib import admin
from .models import *


@admin.register(ViscosityKinematic)
class NoteAdmin(admin.ModelAdmin):
    """Выводит в админ-панель таблицу ViscosityMJL (Измерение кинематической вязкости)"""

    def save_model(self, request, obj, form, change):
        """Функция сигнал для автозаполнения: автор записи = авторизованный пользователь"""

        if not obj.pk:
            obj.performer = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comments)
class NoteAdmin(admin.ModelAdmin):
    """Выводит в админ-панель таблицу Comments (Комментарий к измерению кинематики)"""

    def save_model(self, request, obj, form, change):
        """Функция сигнал для автозаполнения: автор комментария = авторизованный пользователь"""
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)


# admin.site.register(Constants)
