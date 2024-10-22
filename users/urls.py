from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from users import views as UserView
from django.contrib.auth import views as authViews
from . import views

urlpatterns = [
    path('employeeupdate/<str:str>/', views.EmployeeUpdateView, name='employeeupdate'),
    path('employees/', UserView.EmployeesView.as_view(), name='employees'),
    path('companyupdate/', UserView.CompanyUpdateView, name='companyupdate'),
    # path('register/', UserView.register, name='reg'), CompanyProfileView
    path('companyprofile/', UserView.CompanyProfileView.as_view(), name='companyprofile'),
    path('profile/', UserView.ProfileView.as_view(), name='profile'),
    path('login/', authViews.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('profileupdate/', UserView.profileupdate, name='profileupdate'),
    path('password_reset/',
    PasswordResetView.as_view(template_name='users/password_reset_form.html',
                               subject_template_name='users/password_reset_subject.html',
                                email_template_name ='users/password_reset_email.html'),
                                name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_email.html'),
                                                               name='password_reset_done'),
    path('/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
                                                                      name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'),
                                                                   name='password_reset_complete'),
        ]

