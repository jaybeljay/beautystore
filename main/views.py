from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView
from django.urls import reverse, reverse_lazy

from .models import Profile
from .forms import CreateUserForm, UpdateUserForm, UpdateProfileForm


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        
        if request.method == 'POST':
        
            form = CreateUserForm(request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Account was successfully created!')
                return redirect('login')
            else:
                print(form.errors)
                
        return render(request, 'main/register.html', {'form': form})
    

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
                return render(request, 'main/login.html')
                
        return render(request, 'main/login.html')
    

def logoutPage(request):
    logout(request)
    return redirect('login')
    

class UserAccount(DetailView):
    model = Profile
    template_name = 'main/user_account.html'
    context_object_name = 'account'


class EditUserAccount(View):
    template_name = 'main/edit_user_account.html'
    
    def get(self, request, pk):
        user = request.user
        profile = Profile.objects.get(user=user)
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=profile)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form,
                                                    'user': user, 'profile': profile})
        
    def post(self, request, pk):
        user = request.user
        profile = Profile.objects.get(user=user)
        bound_user_form = UpdateUserForm(request.POST, instance=user)
        bound_profile_form = UpdateProfileForm(request.POST, instance=profile)
        if bound_user_form.is_valid() and bound_profile_form.is_valid():
            bound_user_form.save()
            bound_profile_form.save()
        return render(request, self.template_name, {'user_form': bound_user_form, 'profile_form': bound_profile_form,
                                                    'user': user, 'profile': profile})


class DeleteUserAccount(DeleteView):
    model = Profile
    template_name = 'main/delete_user_account.html'
    success_url = reverse_lazy('home')
