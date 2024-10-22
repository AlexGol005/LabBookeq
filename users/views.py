from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUdateForm, ProfileUdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *




@login_required
def profileupdate(request):
    if request.method == "POST":
        profailForm = ProfileUdateForm(request.POST, request.FILES,  instance=request.user.profile)
        userUpdadeForm = UserUdateForm(request.POST, instance=request.user)
        if profailForm.is_valid() and userUpdadeForm.is_valid():
            profailForm.save()
            userUpdadeForm.save()
            messages.success(request, f'данные были успешно обновлены')
            return redirect('profile')

    else:
        profailForm = ProfileUdateForm(instance=request.user.profile)
        userUpdadeForm = UserUdateForm(instance=request.user)
        try:
            user = User.objects.get(username=request.user)
            if user.is_superuser:
                USER = True
            if not user.is_superuser:
                USER = False
        except:
            USER = False

    data = {'profailForm': profailForm,
            'userUpdadeForm': userUpdadeForm,
            'USER': USER
            }

    return render(request, 'users/profileupdate.html', data)

class ProfileView(LoginRequiredMixin, TemplateView):
    """выводит персональную страницу """
    template_name = 'users/profile.html'
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_staff:
                context['USER'] = True
                context['USERTITLE'] = "Продвинутый пользователь"
            if user.is_superuser:
                context['USER'] = True
                context['USERTITLE'] = "Суперпользователь"
            else:
                context['USER'] = False
                context['USERTITLE'] = "Базовый пользователь"
        except:
            context['USER'] = False
        employees = Employees.objects.filter(userid=user.profile.userid)
        company = Company.objects.get(userid=user.profile.userid)
        context['employees'] = employees
        context['company'] = company 
            
        return context



# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Пользовать {username} был успешно создан!')
#             return redirect('home')
#     else:
#         form = UserRegisterForm()

#     return render(
#         request,
#         'users/passwords.html',
#         {
#             'title': 'Страница регистрации',
#             'form': form
#         })
