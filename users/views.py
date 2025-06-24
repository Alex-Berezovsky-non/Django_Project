from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .forms import UserLoginForm, UserRegisterForm, UserProfileUpdateForm, ProfileUpdateForm
from .models import Profile
from django.core.mail import send_mail
from django.http import HttpResponse

User = get_user_model()

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
        user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(self.request, user)
        
        # Создаем профиль пользователя при регистрации
        Profile.objects.create(user=user)
        
        messages.success(self.request, '🎉 Регистрация прошла успешно! Добро пожаловать!')
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
        messages.success(self.request, f'✅ Вход выполнен успешно! Добро пожаловать, {self.request.user.username}!')
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure()
        ):
            return next_url
        return reverse_lazy('landing')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в систему'
        return context

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('landing')
    template_name = 'users/logout.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, '👋 Вы успешно вышли из системы. До новых встреч!')
        return super().dispatch(request, *args, **kwargs)

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile_detail.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self.request.user, 'profile'):
            Profile.objects.create(user=self.request.user)
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = 'users/profile_update_form.html'
    success_url = reverse_lazy('users:profile_detail')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self.request.user, 'profile'):
            Profile.objects.create(user=self.request.user)
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect(self.success_url)
        
        return self.render_to_response(self.get_context_data(
            form=user_form,
            profile_form=profile_form
        ))

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:profile_detail')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ваш пароль был успешно изменен!')
        return super().form_valid(form)

