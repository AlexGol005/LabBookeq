from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from bdanswers.forms import SearchForm
from bdanswers.models import Bdanswers


# Create your views here.
class BdanswersQestionView(View):
    """ выводит отдельный вопрос на билет"""
    def get(self, request, str):
        note = Bdanswers.objects.get(number=str)

        context = {
            'note': note,
        }
        return render(request, 'bdanswers/bdanswer.html', context)


class BdanswersAll(TemplateView):
    """выводит заглавную страницу и поисковик билетов """
    template_name = 'bdanswers/bdanswersall.html'

    def get_context_data(self, **kwargs):
        context = super(BdanswersAll, self).get_context_data(**kwargs)
        context['formSM'] = SearchForm
        return context


class SearchResultView(TemplateView):
    """выводит результаты поиска по билетам"""
    template_name = 'bdanswers/bdresult.html'
    def get_context_data(self, **kwargs):
        name = self.request.GET['name']
        context = super(SearchResultView, self).get_context_data(**kwargs)
        objects = Bdanswers.objects.filter(question=name)
        context['objects'] = objects
        context['formSM'] = SearchForm
        return context


class BdanswersListView(ListView):
    """ Выводит список всех билетов пагинированный по 1 билету на страницу """
    model = Bdanswers
    template_name = 'bdanswers/bdanswerslist.html'
    context_object_name = 'objects'
    paginate_by = 1

