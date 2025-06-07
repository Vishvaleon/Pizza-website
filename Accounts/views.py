from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.shortcuts import redirect

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Save the user first
        user = form.save()
        
        # Automatically log in the user
        login(self.request, user)
    
        # Redirect to the desired page
        return redirect(self.success_url)