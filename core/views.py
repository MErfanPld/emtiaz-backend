from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic import FormView

# Create your views here.

class HomeView(TemplateView):
    template_name = "./core/home.html"    
