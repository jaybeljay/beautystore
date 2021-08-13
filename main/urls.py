from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import registerPage, loginPage, logoutPage, UserAccount, EditUserAccount, DeleteUserAccount

urlpatterns = [
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('account/<int:pk>/', login_required(UserAccount.as_view()), name='account'),
    path('account/<int:pk>/edit/', login_required(EditUserAccount.as_view()), name='edit_account'),
    path('account/<int:pk>/delete/', login_required(DeleteUserAccount.as_view()), name='delete_account'),
]