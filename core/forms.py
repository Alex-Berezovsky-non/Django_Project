from django import forms
from .models import Review, Master

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