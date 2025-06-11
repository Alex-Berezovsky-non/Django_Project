from django import forms
from .models import Review, Master, Order, Service

class ReviewForm(forms.ModelForm):
    master = forms.ModelChoiceField(
        queryset=Master.objects.all(),
        label="Мастер",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Review
        fields = ['client_name', 'text', 'rating', 'master', 'photo']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.NumberInput(attrs={
                'class': 'd-none',
                'min': 1,
                'max': 5,
                'type': 'number'
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'client_name': 'Ваше имя',
            'text': 'Текст отзыва',
            'rating': 'Оценка',
            'photo': 'Фото (необязательно)'
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'master', 'services', 'appointment_date', 'comment']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-select'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'client_name': 'Имя клиента',
            'phone': 'Телефон',
            'master': 'Мастер',
            'services': 'Услуги',
            'appointment_date': 'Дата и время записи',
            'comment': 'Комментарий'
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название услуги',
            'description': 'Описание',
            'price': 'Цена',
            'duration': 'Длительность (мин)',
            'is_popular': 'Популярная услуга',
            'image': 'Изображение'
        }

class ServiceEasyForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название услуги',
            'price': 'Цена',
        }