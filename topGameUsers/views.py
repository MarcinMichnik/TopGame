from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError   
from django.db.models import Sum
from datetime import timedelta, datetime
from django.utils import timezone 
from django.db.models import Count
from django.views.generic import (TemplateView,
                                       ListView,
                                       DetailView,
                                       UpdateView,
                                       CreateView,
                                       DeleteView)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'GET':
        return render(
            request, 'topGameUsers/register.html',
            {'form': CustomUserCreationForm}
        )
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard'))
        
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Konto zostało zaktualizowane.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    
    return render(request, 'topGameUsers/profile.html', context)