from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    telegram_id = models.CharField(max_length=50, blank=True)
    github_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"