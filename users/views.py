from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUdateForm, ProfileUdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from equipment.models import *



@login_required
def profileupdate(request):
    ProfileUdateForm = ProfileUdateForm()
    if request.method == "POST":
        ProfileUdateForm = ProfileUdateForm(request.POST, request.FILES,  instance=request.user.profile)
        if ProfileUdateForm.is_valid():
            ProfileUdateForm.save()
            messages.success(request, f'данные были успешно обновлены')
            return redirect('profile')

    # else:
    #     profailForm = ProfileUdateForm(instance=request.user.profile)
    #     userUpdadeForm = UserUdateForm(instance=request.user)
    #     try:
    #         user = User.objects.get(username=request.user)
    #         if user.is_superuser:
    #             USER = True
    #         if not user.is_superuser:
    #             USER = False
    #     except:
    #         USER = False

        data = {'ProfileUdateForm': ProfileUdateForm,
                }

        return render(request, 'users/profileupdate.html', data)
    else:
        ProfileUdateForm = ProfileUdateForm(instance=request.user.profile)
        # userUpdadeForm = UserUdateForm(instance=request.user)

    data = {
            'ProfileUdateForm': ProfileUdateForm,
            }
    # 'userUpdadeForm': userUpdadeForm


    return render(request, 'users/profile.html', data)

class ProfileView(LoginRequiredMixin, TemplateView):
    """выводит персональную страницу """
    template_name = 'users/profile.html'
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        l = user.groups.values_list('name',flat = True) 
        try:
            user_group = list(l)[0]
        except:
             user_group = 'Суперпользователь'
            
        employees = Employees.objects.filter(userid__userid=user.profile.userid)
        company = Company.objects.get(userid=user.profile.userid)
        context['employees'] = employees
        context['company'] = company 
        context['user_group'] = user_group 
        context['ProfileUdateForm'] = ProfileUdateForm() 
            
        return context



class CompanyProfileView(LoginRequiredMixin, TemplateView):
    """выводит страницу данных компании """
    template_name = 'users/companyprofile.html'
    def get_context_data(self, **kwargs):
        context = super(CompanyProfileView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_staff or user.is_superuser:
                context['USER'] = True
            else:
                context['USER'] = False
        except:
            context['USER'] = False
        employees = Employees.objects.filter(userid__userid=user.profile.userid)
        company = Company.objects.get(userid=user.profile.userid)
        context['employees'] = employees
        context['company'] = company 
            
        return context


@login_required
def CompanyUpdateView(request):
    """выводит форму для обновления данных о компании"""
    uruser = request.user
    ruser = request.user.profile.userid
    if uruser.has_perm('equipment.add_equipment') or uruser.is_superuser:
        
        if request.method == "POST":
            form = CompanyCreateForm(request.POST, instance=Company.objects.get(userid=ruser))
            if form.is_valid():

                n = Agreementverification.objects.get_or_create(active=True, company=Company.objects.get(userid=ruser), verificator=Verificators.objects.get(pk=14), pointer=ruser)
                order = form.save(commit=False)
                order.save() 
                               
                return redirect('companyprofile')
        else:
            form = CompanyCreateForm(instance=Company.objects.get(userid=ruser))
        data = {'form': form,}               
        return render(request, 'equipment/reg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел недоступен')
        return redirect('companyupdate')


class EmployeesView(LoginRequiredMixin, TemplateView):
    """выводит страницу сотрудников компании """
    template_name = 'users/employees.html'
    def get_context_data(self, **kwargs):
        context = super(EmployeesView, self).get_context_data(**kwargs)
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_staff or user.is_superuser:
                context['USER'] = True
            else:
                context['USER'] = False
        except:
            context['USER'] = False
        employees = Employees.objects.filter(userid__userid=user.profile.userid)
        company = Company.objects.get(userid=user.profile.userid)
        context['employees'] = employees
        context['company'] = company 
            
        return context

def EmployeeUpdateView(request, str):
    """выводит форму для обновления данных о сотруднике"""
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = EmployeesUpdateForm(request.POST, instance=Employees.objects.get(pk=str))                                                       
            if form.is_valid():
                order = form.save(commit=False)
                order.save()
                return redirect('employees')
        else:
            form = EmployeesUpdateForm(instance=Employees.objects.get(pk=str))
        data = {'form': form,}                
        return render(request, 'equipment/reg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел недоступен')
        return redirect('employees')



@login_required
def Employeereg(request):
    """выводит форму для регистрации  сотрудника"""
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
        if request.method == "POST":
            form = EmployeesUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                order = form.save(commit=False)
                order.userid = Company.objects.get(userid=request.user.profile.userid)
                order.save()
                return redirect('employees')
        else:
            form = EmployeesUpdateForm()
        data = {'form': form, }                   
        return render(request, 'equipment/reg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел недоступен')
        return redirect('employees')

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
