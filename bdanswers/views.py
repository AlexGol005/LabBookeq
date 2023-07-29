from django.shortcuts import render
from django.views import View

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
