from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import UserRegisterView, UserLoginView, UserLogoutView,UserProfileDetailView,UserProfileUpdateView,UserPasswordChangeView

app_name = 'users'

urlpatterns = [
    # Основные пути аутентификации
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # Восстановление пароля
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.txt',
            success_url=reverse_lazy('users:password_reset_done')
        ), 
        name='password_reset'),
    
    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ), 
        name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')
        ), 
        name='password_reset_confirm'),
    
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ), 
        name='password_reset_complete'),
        path('profile/', UserProfileDetailView.as_view(), name='profile_detail'),
        path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),
        path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
        
]