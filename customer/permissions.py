
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View
import rules
    
class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
