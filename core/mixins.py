# core/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest
from typing import cast

class StaffRequiredMixin(UserPassesTestMixin):
    request: HttpRequest
    
    def test_func(self) -> bool:
        if not hasattr(self, 'request'):
            return False
        return cast(bool, self.request.user.is_staff)