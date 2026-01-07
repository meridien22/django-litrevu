from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import forms
from authentication.forms import UserFollowerToAddForm, UserFollowersForm
from authentication.models import User

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

@login_required     
def logout_user(request):
    logout(request)
    messages.error(request, "Vous êtes déconnecté")
    return redirect('home')

@login_required
def abonnements(request):
    if request.method == 'POST':
        if "add_follower" in request.POST:
            form = UserFollowerToAddForm(request.POST, user=request.user)
            if form.is_valid():
                abonnement = form.save(commit=False)
                abonnement.user = request.user
                abonnement.save()
                return redirect("abonnements")
        if "delete_follower" in request.POST:
            UserFollows = User.objects.get(id=request.POST["followed_user"])
            UserFollows.delete()
            return redirect("abonnements")


    form = UserFollowerToAddForm(user=request.user)

    userFollows = request.user.following.all()
    userFollows_forms = []
    for userFollow in userFollows:
        formFollow = UserFollowersForm(instance=userFollow)
        userFollows_forms.append(formFollow)

    return render(request, "authentication/abonnements.html", context={
    'form': form,
    'userFollows_forms': userFollows_forms
    })


