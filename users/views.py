from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.management.utils import get_random_secret_key

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, UserUdateForm, ProfileUdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from equipment.models import *





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
        context['ProfileUdateForm'] = ProfileUdateForm(self.request.POST, self.request.FILES,  instance=self.request.user.profile) 
            
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if context['ProfileUdateForm'].is_valid():
            order = context['ProfileUdateForm'].save(commit=False)
            order.save()
            return redirect('profile')

        else:
            messages.success(self.request, "Раздел доступен только продвинутому пользователю")
            return redirect('profile')



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
    """path('employees/', UserView.EmployeesView.as_view(), name='employees'),"""
    
    template_name = 'users/employees.html'
    
    def get_context_data(self, **kwargs):
        context = super(EmployeesView, self).get_context_data(**kwargs)
        employees = User.objects.filter(profile__userid=self.request.user.profile.userid)
        company = Company.objects.get(userid=self.request.user.profile.userid)
        context['employees'] = employees
        context['company'] = company 
   
            
        return context






# @login_required
# def Employeereg(request):
#     """выводит форму для регистрации  сотрудника"""
#     if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
#         if request.method == "POST":
#             form = EmployeesUpdateForm(request.POST, request.FILES)
#             if form.is_valid():
#                 order = form.save(commit=False)
#                 order.userid = Company.objects.get(userid=request.user.profile.userid)
#                 order.save()
#                 return redirect('employees')
#         else:
#             form = EmployeesUpdateForm()
#         data = {'form': form, }                   
#         return render(request, 'equipment/reg.html', data)
#     if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
#         messages.success(request, 'Раздел недоступен')
#         return redirect('employees')


@login_required
def Employeereg(request):
    """выводит форму для добавления пользователя (сотрудника) и его профиля"""
    path('employeereg/', views.Employeereg, name='employeereg'),
    
    if request.method == "POST":
        group_name = 'Базовый пользователь'
        if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
            form = UserRegisterForm(request.POST)
            form1 = ProfileRegisterForm(request.POST) 
            if form.is_valid() and form1.is_valid():
                u_f = form.save()
                p_f = form1.save(commit=False)
                p_f.user_id = u_f.id
                p_f.userid = request.user.profile.userid
                p_f.save()              
                g = Group.objects.get(name=group_name)
                g.user_set.add(u_f)
                username = form.cleaned_data.get('username')
                messages.success(request, f'Пользовать {username} был успешно создан!')
                return redirect('employees')
            else:
                messages.add_message(request, messages.ERROR, form.errors)
                return redirect('employees')
                
        else:
            messages.success(request, 'Раздел доступен только продвинутому пользователю')
            return redirect('employees')
    else:
        form = UserRegisterForm()
        form1 = ProfileRegisterForm()
        data =         {
            'title': 'Страница регистрации',
            'form': form,
            'form1': form1,
        }
        return render(request,  'users/reg.html', data)
        
       
def EmployeeUpdateView(request, str):
    """выводит форму для обновления данных о сотруднике"""
    """path('employeeupdate/<str:str>/', views.EmployeeUpdateView, name='employeeupdate'),"""
    
    if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:

        if request.method == "POST":
            form = UserUdateForm(request.POST, instance=User.objects.get(pk=str))
            form1 = ProfileRegisterForm(request.POST, instance=Profile.objects.get(user__pk=str)) 
                                                          
            if form.is_valid() and form1.is_valid():
                order = form.save(commit=False)
                order1 = form1.save(commit=False)
                order.save()                
                order1.save()
                return redirect('employees')
        else:
            form = UserUdateForm(instance=User.objects.get(pk=str))
            form1 = ProfileRegisterForm(instance=Profile.objects.get(user__pk=str)) 
        data = {'form': form,
                'form1': form1,
               }                
        return render(request, 'users/reg.html', data)
    if not request.user.has_perm('equipment.add_equipment') or not request.user.is_superuser:
        messages.success(request, 'Раздел доступен только продвинутому пользователю')
        return redirect('employees')




# @login_required
# def HeadEmployeereg(request):
#     """выводит форму для добавления первого сотрудника и вместе с ним - профиля компании"""
#     """path('heademployeereg/', views.HeadEmployeereg, name='heademployeereg'),"""
    
#     if request.method == "POST":
#         group_name = 'Продвинутый пользователь'
#         form = UserRegisterForm(request.POST)
#         form1 = ProfileRegisterForm(request.POST) 
#         if form.is_valid() and form1.is_valid():
#             u_f = form.save()
#             p_f = form1.save(commit=False)
#             p_f.user_id = u_f.id
#             p_f.userid = get_random_secret_key()
#             newuserid =  p_f.userid
#             p_f.save()              
#             g = Group.objects.get(name=group_name)
#             g.user_set.add(u_f)
#             name_prima = f'замените на название Вашей организации - {newuserid}'

#             newcompany = Company.objects.get_or_create(userid=newuserid, pay = False, name=name_prima, name_big=name_prima)

            
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Пользовать {username} был успешно создан!')
#             return redirect('profile')
#         else:
#             messages.add_message(request, messages.ERROR, form.errors)
#             return redirect('heademployeereg')
                
#     else:
#         form = UserRegisterForm()
#         form1 = ProfileRegisterForm()
#         data =         {
#             'title': 'Страница регистрации',
#             'form': form,
#             'form1': form1,
#         }
#         return render(request,  'users/reg.html', data)



@login_required
def HeadEmployeereg(request):
    """выводит форму для добавления первого сотрудника и вместе с ним - профиля компании"""
    """path('heademployeereg/', views.HeadEmployeereg, name='heademployeereg'),"""
    
    if request.method == "POST":
        group_name = 'Продвинутый пользователь'
        form = UserRegisterForm(request.POST)

        if form.is_valid() :
            u_f = form.save()
             
            g = Group.objects.get(name=group_name)
            g.user_set.add(u_f)
            


            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользовать {username} был успешно создан!')
            return redirect('profile')
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return redirect('heademployeereg')
                
    else:
        form = UserRegisterForm()

        data =         {
            'title': 'Страница регистрации',
            'form': form,

        }
        return render(request,  'users/reg.html', data)
