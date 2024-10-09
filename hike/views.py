from datetime import date

from django.shortcuts import render
import pandas as pd
from django.views.generic import ListView, CreateView

from django.db.models import Q


from .models import *
from .forms import *
from .constants import *
from django.views.generic import ListView, TemplateView, CreateView, UpdateView

now = date.today()

def index(request):
    """ view function for sales app """

    # read data                                                                                                  
	
    df = pd.read_csv('hike/car_sales.csv')
    rs = df.groupby("Engine size")["Sales in thousands"].agg("sum")
    categories = list(rs.index)
    values = list(rs.values)
	
    table_content = df.to_html(index=None)
    table_content = table_content.replace("","")
    table_content = table_content.replace('class="dataframe"',"class='table table-striped'")
    table_content = table_content.replace('border="1"',"")
	
    context = {"categories": categories, 'values': values, 'table_data':table_content}
    return render(request, 'hike/example.html', context=context)

class ExampleTemplateView(TemplateView):
    template_name = 'hike/example.html'

class HikeAllListView(ListView):
    """ Выводит список всех маршрутов """
    model = Hike
    template_name = 'hike/mainlist.html'
    context_object_name = 'objects'
    ordering = ['-pk']
    paginate_by = 6
    def get_context_data(self,**kwargs):
        context = super(HikeAllListView,self).get_context_data(**kwargs)
        context['form'] = SearchForm() 
        context['pk'] = 0
        context['qk'] = 0
        context['rk'] = 0
        return context



class BMAllListView(ListView):
    """ Выводит список всех закладок на разные темы """
    model = Bookmarks
    template_name = 'hike/bm.html'
    context_object_name = 'objects'
    ordering = ['-pk']
    paginate_by = 6
    def get_queryset(self):
        return Bookmarks.objects.filter(done=False).order_by('-pk')
    def get_context_data(self,**kwargs):
        context = super(BMAllListView,self).get_context_data(**kwargs)
        context['form'] = UdateForm()
        context['sform'] = SearchForm() 
        return context

class BMSearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска по истории Карелии """

    template_name = 'hike/bm.html'

    def get_context_data(self, **kwargs):
        context = super(BMSearchResultView, self).get_context_data(**kwargs)
        searchword = self.request.GET['searchword']
        context['form'] = UdateForm()
        context['sform'] = SearchForm() 
        if self.request.GET['searchword']:
            searchword1 = self.request.GET['searchword'][0].upper() + self.request.GET['searchword'][1:]
        if searchword:
            objects = Bookmarks.objects.\
            filter(Q(text__icontains=searchword)|Q(text__icontains=searchword1)).order_by('pk')
            context['objects'] = objects
            
        return context



class ITAllListView(ListView):
    """ Выводит список всех закладок по айти """
    model = Itbookmarks
    template_name = 'hike/it.html'
    context_object_name = 'objects'
    ordering = ['-pk']
    paginate_by = 6
    def get_context_data(self,**kwargs):
        context = super(ITAllListView,self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context

class KareliahistoryAllListView(ListView):
    """ Выводит список всех закладок по истории Карелии """
    model = Kareliahistory
    template_name = 'hike/kareliahistory.html'
    context_object_name = 'objects'
    ordering = ['-pk']
    paginate_by = 6
    def get_context_data(self,**kwargs):
        context = super(KareliahistoryAllListView,self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context

class KareliahistorySearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска по истории Карелии """

    template_name = 'hike/kareliahistory.html'

    def get_context_data(self, **kwargs):
        context = super(KareliahistorySearchResultView, self).get_context_data(**kwargs)
        searchword = self.request.GET['searchword']
        context['form'] = SearchForm()
        if self.request.GET['searchword']:
            searchword1 = self.request.GET['searchword'][0].upper() + self.request.GET['searchword'][1:]
        if searchword:
            objects = Kareliahistory.objects.\
            filter(Q(title__icontains=searchword)|Q(title__icontains=searchword1)).order_by('pk') | Kareliahistory.objects.\
            filter(Q(text__icontains=searchword)|Q(text__icontains=searchword1)).order_by('pk')
            context['objects'] = objects
            
        return context


class HikeStrView(CreateView):
    """ выводит отдельный маршрут """
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


class SearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска по слову/фразе в списке маршрутов """

    template_name = 'hike/mainlist.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        searchword = self.request.GET['searchword']
        if self.request.GET['searchword']:
            searchword1 = self.request.GET['searchword'][0].upper() + self.request.GET['searchword'][1:]
        if searchword:
            objects = Hike.objects.\
            filter(Q(title__icontains=searchword)|Q(title__icontains=searchword1)).order_by('pk') | Hike.objects.\
            filter(Q(country__icontains=searchword)|Q(country__icontains=searchword1)).order_by('pk') | Hike.objects.\
            filter(Q(region__icontains=searchword)|Q(region__icontains=searchword1)).order_by('pk') | Hike.objects.\
            filter(Q(start_station__icontains=searchword)|Q(start_station__icontains=searchword1)).order_by('pk') | Hike.objects.\
            filter(Q(aim_station__icontains=searchword)|Q(aim_station__icontains=searchword1)).order_by('pk') | Hike.objects.\
            filter(Q(home_station__icontains=searchword)|Q(home_station__icontains=searchword1)).order_by('pk') | Hike.objects.\
            filter(Q(back_station__icontains=searchword)|Q(back_station__icontains=searchword1)).order_by('pk') | Hike.objects.\
            filter(Q(travel_details__icontains=searchword)|Q(travel_details__icontains=searchword1)).order_by('pk') | Hike.objects.\
            filter(Q(attractions__icontains=searchword)|Q(attractions=searchword1)).order_by('pk')
            context['objects'] = objects
            context['form'] = SearchForm(initial={'searchword': searchword})
            context['pk'] = 0
            context['qk'] = 0
            context['rk'] = 0
        return context
        

class ITSearchResultView(TemplateView):
    """ Представление, которое выводит результаты поиска по закладкам айти """

    template_name = 'hike/it.html'

    def get_context_data(self, **kwargs):
        context = super(ITSearchResultView, self).get_context_data(**kwargs)
        searchword = self.request.GET['searchword']
        if self.request.GET['searchword']:
            searchword1 = self.request.GET['searchword'][0].upper() + self.request.GET['searchword'][1:]
        if searchword:
            objects = Itbookmarks.objects.\
            filter(Q(text__icontains=searchword)|Q(text__icontains=searchword1)).order_by('pk')
            context['objects'] = objects
            context['form'] = SearchForm(initial={'searchword': searchword})
        return context



def filterview(request, pk):
    """ Фильтр заметок по темам """
    objects = Bookmarks.objects.filter(done=False)
    for i in range(len(TYPE)):
        s = TYPE[i][0]
        if pk == i:
            objects = objects.filter(type=s).order_by('-pk')
            form = UdateForm()
            sform = SearchForm() 

    return render(request,  "hike/bm.html", {'objects': objects, 'form':form, 'sform':sform})


def hikefilterview(request, pk):
    """ Фильтр пройденных и непройденных маршрутов в этом году """
    ar = str(now.year)[2:]
    arr = f'{ar};'
    if pk == 0:   
        objects = Hike.objects.all()
    if pk == 1:
        objects = Hike.objects.filter(dates_try__iendswith=ar).order_by('-pk') | Hike.objects.filter(dates_try__iendswith=arr).order_by('-pk')
    if pk == 2:   
        objects = Hike.objects.exclude(dates_try__iendswith=ar).order_by('-pk') & Hike.objects.exclude(dates_try__iendswith=arr).order_by('-pk')
    form = SearchForm() 
    qk = 0
    rk = 0
    return render(request,  "hike/mainlist.html", {'objects': objects, 'form':form, 'pk': pk , 'qk': qk, 'rk': rk})

def donehikefilterview(request, qk):
    """ Фильтр пройденных и непройденных маршрутов вообще"""
    if qk == 0:   
        objects = Hike.objects.all()
    if qk == 1:
        objects = Hike.objects.filter(reality=True).order_by('-pk') 
    if qk == 2:   
        objects = Hike.objects.filter(reality=False).order_by('-pk')  
    form = SearchForm() 
    pk = 0
    rk = 0
    return render(request,  "hike/mainlist.html", {'objects': objects, 'form':form, 'pk': pk , 'qk': qk, 'rk': rk})

def readyhikefilterview(request, rk):
    """ Фильтр готовых и не готовых маршрутов"""
    if rk == 0:   
        objects = Hike.objects.all()
    if rk == 1:
        objects = Hike.objects.filter(maturity=True).order_by('-pk') 
    if rk == 2:   
        objects = Hike.objects.filter(maturity=False).order_by('-pk')  
    form = SearchForm() 
    pk = 0
    qk = 0
    return render(request,  "hike/mainlist.html", {'objects': objects, 'form':form, 'pk': pk , 'qk': qk, 'rk': rk})
