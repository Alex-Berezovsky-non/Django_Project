from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
import re
from datetime import date
from .models import Profile
User = get_user_model()

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя или Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя или Email',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'autocomplete': 'current-password'
        }),
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages = {
            'invalid_login': (
                "Пожалуйста, введите правильные имя пользователя/email и пароль. "
                "Оба поля могут быть чувствительны к регистру."
            ),
            'inactive': "Этот аккаунт неактивен.",
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш email',
            'autocomplete': 'email'
        }),
        error_messages={
            'required': 'Пожалуйста, введите ваш email',
            'invalid': 'Введите правильный email адрес',
        }
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': 'Имя пользователя',
        }
        help_texts = {
            'username': 'Только буквы, цифры и @/./+/-/_',
        }
        error_messages = {
            'username': {
                'required': 'Пожалуйста, введите имя пользователя',
                'unique': 'Пользователь с таким именем уже существует',
            },
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Убираем стандартные подсказки Django для паролей
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Настройка полей
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Придумайте имя пользователя',
            'autocomplete': 'username'
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Придумайте пароль',
            'autocomplete': 'new-password'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password'
        })
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("Имя пользователя должно содержать минимум 3 символа")
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise ValidationError("Имя пользователя содержит недопустимые символы")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов")
        
        # Проверка сложности пароля
        if not any(char.isdigit() for char in password1):
            raise ValidationError("Пароль должен содержать хотя бы одну цифру")
            
        if not any(char.isalpha() for char in password1):
            raise ValidationError("Пароль должен содержать хотя бы одну букву")
            
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Пароли не совпадают")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        if commit:
            user.save()
        return user
from datetime import date

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите email'
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'telegram_id', 'github_id']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telegram_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            'github_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username'
            }),
        }
        help_texts = {
            'telegram_id': 'Введите ваш Telegram ID (начинается с @)',
            'github_id': 'Введите ваш GitHub username',
        }
    
    def clean_telegram_id(self):
        telegram_id = self.cleaned_data.get('telegram_id')
        if telegram_id and not telegram_id.startswith('@'):
            raise ValidationError("Telegram ID должен начинаться с @")
        return telegram_id
    
    def clean_github_id(self):
        github_id = self.cleaned_data.get('github_id')
        if github_id and ' ' in github_id:
            raise ValidationError("Github ID не должен содержать пробелов")
        return github_id
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > date.today():
            raise ValidationError("Дата рождения не может быть в будущем")
        return birth_date