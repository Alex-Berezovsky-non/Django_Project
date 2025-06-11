from django import forms
from .models import Review, Master, Order, Service

class ReviewForm(forms.ModelForm):
    master = forms.ModelChoiceField(
        queryset=Master.objects.filter(is_active=True),
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
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше полное имя'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 999-99-99'
            }),
            'master': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_master'
            }),
            'services': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'id': 'id_services'
            }),
            'appointment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваши пожелания...'
            }),
        }
        labels = {
            'client_name': 'Ваше имя',
            'phone': 'Телефон',
            'master': 'Мастер',
            'services': 'Услуги',
            'appointment_date': 'Дата и время записи',
            'comment': 'Комментарий (необязательно)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['master'].queryset = Master.objects.filter(is_active=True)
        self.fields['services'].queryset = Service.objects.all()

        self.fields['client_name'].required = True
        self.fields['phone'].required = True
        self.fields['master'].required = True
        self.fields['services'].required = True
        self.fields['appointment_date'].required = True

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_popular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название услуги',
            'description': 'Описание',
            'price': 'Цена (руб.)',
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
            'price': 'Цена (руб.)',
        }