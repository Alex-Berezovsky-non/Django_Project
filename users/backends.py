from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Пытаемся найти пользователя по email
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Если пользователь не найден, возвращаем None
            return None
        except User.MultipleObjectsReturned:
            # Если найдено несколько пользователей с одинаковым email
            return None