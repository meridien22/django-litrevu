from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages

from . import forms

class SignUp(View):
    template_name = 'authentication/signup.html'
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            messages.success(request, "L'inscription a réussie")
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, "L'inscription a échouée")
            return render(request, self.template_name, context={'form': form})
        

class LoginPage(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                messages.success(request, "La connexion a réussie")
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, "La connexion a échouée")
                return render(request, self.template_name, context={'form': form})
        else:
            messages.error(request, "Les informations fournies de sont pas correctes")
            return render(request, self.template_name, context={'form': form})
        
def logout_user(request):
    logout(request)
    messages.error(request, "Vous êtes déconnecté")
    return redirect('home')