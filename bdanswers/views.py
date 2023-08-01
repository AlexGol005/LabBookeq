from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from bdanswers.models import Bdanswers


# Create your views here.
class BdanswersQestionView(View):
    """ выводит отдельную вопрос на билет"""
    def get(self, request, str):
        note = Bdanswers.objects.get(number=str)

        context = {
            'note': note,
        }
        return render(request, 'bdanswers/bdquestion.html', context)


class BdanswersAll(TemplateView):
    """выводит заглавную страницу и поисковик билетов """
    template_name = 'users/personal.html'