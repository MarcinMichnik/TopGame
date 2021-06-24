from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError   
from datetime import timedelta, datetime
from django.utils import timezone 
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm, RuneCreationForm
from django.contrib import messages
from .models import Mana, Rune
from json import dumps
from django.db.models import Avg, Count, Min, Sum

class Register(TemplateView):
    template_name = 'topGameUsers/register.html'
    
    def get(self, request, *args, **kwargs):
        return render(
            request, 'topGameUsers/register.html',
            {'form': CustomUserCreationForm}
        )
    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard'))

        
class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'topGameUsers/profile.html'
    
    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
        context = {
            'u_form':u_form,
            'p_form':p_form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Konto zostało zaktualizowane.')
            return redirect('profile')
        
        context = {
            'u_form':u_form,
            'p_form':p_form
        }
        
        return render(request, self.template_name, context)

class UserStatistics(LoginRequiredMixin, TemplateView):
    template_name = 'topGameUsers/statistics.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        
        user_manas = self.getUserManaRecords(request)
        context['user_manas'] = user_manas
        
        current_mana_sum = self.getCurrentUserManaSum(request)
        context['current_mana_sum'] = current_mana_sum
        
        #import pdb; pdb.set_trace()

        return render(request, self.template_name, context)
    
    def getUserManaRecords(self, request):
        result = []
        timezone_index = datetime.today() + timedelta(days=-11)
        for i in range(11):
            timezone_index += timedelta(days=1)
            manas = Mana.objects.filter(belongs_to=request.user, date_of_assignment__lte=timezone_index)
            
            x_value = str(timezone_index.date())
            y_value = manas.aggregate(power_sum=Sum('power'))['power_sum']
            
            if y_value is None:
                y_value = 0
            
            result.append({'x':x_value, 'y':y_value}) 
            
        return result
    
    def getCurrentUserManaSum(self, request):
        current_user_manas = Mana.objects.filter(belongs_to=request.user)
        current_user_mana_sum = current_user_manas.aggregate(all_user_power_sum=Sum('power'))['all_user_power_sum']
        
        return current_user_mana_sum
    
class Shop(LoginRequiredMixin, TemplateView):
    model = Rune
    template_name = 'topGameUsers/shop.html'
    
    def get(self, request, *args, **kwargs):
        rune_form = RuneCreationForm(instance=request.user)
        runes = Rune.objects.filter(belongs_to=request.user)
        
        current_mana_sum = self.getCurrentUserManaSum(request)
        
        context = {'runes':runes, 'rune_form':rune_form, 'current_mana_sum':current_mana_sum}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        rune_form = RuneCreationForm(request.POST)
        runes = Rune.objects.filter(belongs_to=request.user)
        current_mana_sum = self.getCurrentUserManaSum(request)
        context = {'runes':runes, 'rune_form':rune_form, 'current_mana_sum':current_mana_sum}
        
        #import pdb; pdb.set_trace()
        
        rune_form.instance.belongs_to = request.user
        rune_form.instance.date_of_assignment = datetime.now()
        if rune_form.is_valid():
            rune_form.save()
            
            subtract_mana = Mana.objects.latest('date_of_assignment')
            subtract_mana.power -= int(request.POST['power'])
            subtract_mana.save()
            
            messages.success(request, f'The rune has been created successfuly.')
            return redirect('shop')
        
        return render(request, self.template_name, context)
    
    def getCurrentUserManaSum(self, request):
        current_user_manas = Mana.objects.filter(belongs_to=request.user)
        current_user_mana_sum = current_user_manas.aggregate(all_user_power_sum=Sum('power'))['all_user_power_sum']
        
        return current_user_mana_sum