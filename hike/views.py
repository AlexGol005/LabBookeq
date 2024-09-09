from django.shortcuts import render

from django.views.generic import ListView, CreateView


from .models import *
from .forms import *
from .constants import *


class HikeAllListView(ListView):
    """ Выводит список всех постов """
    model = Hike
    template_name = 'hike/mainlist.html'
    context_object_name = 'objects'
    ordering = ['-pk']
    paginate_by = 6
    def get_context_data(self,**kwargs):
        context = super(HikeAllListView,self).get_context_data(**kwargs)
        context['title'] = TITLE
        return context


class BMAllListView(ListView):
    """ Выводит список всех постов """
    model = Bookmarks
    template_name = 'hike/bm.html'
    context_object_name = 'objects'
    ordering = ['-pk']
    paginate_by = 6
    def get_context_data(self,**kwargs):
        context = super(BMAllListView,self).get_context_data(**kwargs)
        context['title'] = TITLE
        return context

class HikeStrView(CreateView):
    """ выводит отдельный пост """
    model = Hike
    template_name = 'hike/indilist.html'
    form_class = CommentCreationForm

    def get_object(self, queryset=None):
        return Hike.objects.get(pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super(HikeStrView, self).get_context_data(**kwargs)
        comments = Comments.objects.filter(forNote=self.kwargs['pk']).order_by("pk")
        obj = Hike.objects.get(pk=self.kwargs.get("pk"))
        context['form'] = CommentCreationForm()
        context['comments'] = comments
        context['obj'] = obj

        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.forNote = Hike.objects.get(pk=self.kwargs['pk'])
        order.save()
        return super().form_valid(form)
