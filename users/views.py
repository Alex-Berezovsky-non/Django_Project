# users/views.py
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserLoginForm, UserRegisterForm

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('landing')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Регистрация прошла успешно! Добро пожаловать!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        messages.success(self.request, f'Добро пожаловать, {self.request.user.username}!')
        next_url = self.request.GET.get('next')
        return next_url or reverse_lazy('landing')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в систему'
        return context

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('landing')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Вы успешно вышли из системы')
        return super().dispatch(request, *args, **kwargs)