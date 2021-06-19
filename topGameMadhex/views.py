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
#from .models import ()

class MadhexView(TemplateView):
    template_name = 'topGameMadhex/madhex_play.html'