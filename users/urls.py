from django.urls import path, re_path, reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,\
    PasswordResetConfirmView, PasswordResetCompleteView
from . import views


app_name = 'users'


urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit'),
    path('change_password', views.change_password, name='change_password'),
    path('reset_password', PasswordResetView.as_view(template_name='authenticate/reset_password.html',
                                                     success_url=reverse_lazy('users:password_reset_done')),
         name='reset_password'),
    path('reset_password/done', PasswordResetDoneView.as_view(template_name='authenticate/reset_password_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='authenticate/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(template_name='authenticate/reset_password_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]