from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Profile

    
class UserCheckMixin(LoginRequiredMixin, UserPassesTestMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
        
    def test_func(self, request):
        return self.request.user=
