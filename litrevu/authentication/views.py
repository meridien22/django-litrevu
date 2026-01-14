from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . import forms
from authentication.forms import UserFollowerToAddForm, UserFollowersForm
from authentication.models import UserFollows


class SignUp(View):
    """View allowing the creation of a new user.

    Args:
        View : Base class for creating views.
    """
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
    """A view allowing a user to log in.

    Args:
        View : Base class for creating views.
    """
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
    """View allowing a user to log out."""

    logout(request)
    messages.error(request, "Vous êtes déconnecté")
    return redirect('home')


@login_required
def abonnements(request):
    """A view allowing a user to follow or unfollow other users."""

    if request.method == 'POST':
        if "add_follower" in request.POST:
            form = UserFollowerToAddForm(request.POST, user=request.user)
            if form.is_valid():
                abonnement = form.save(commit=False)
                abonnement.user = request.user
                abonnement.save()
                return redirect("abonnements")
        if "delete_follower" in request.POST:
            print(request.POST["followed_user"])
            UserFollow = UserFollows.objects.get(followed_user_id=request.POST["followed_user"],
                                                 user_id=request.user)
            UserFollow.delete()
            return redirect("abonnements")

    userFollowsAdd_forms = UserFollowerToAddForm(user=request.user)

    userFollowsByMe = request.user.following.all()
    userFollowsByMe_forms = []
    for userFollowByMe in userFollowsByMe:
        formFollow = UserFollowersForm(instance=userFollowByMe)
        userFollowsByMe_forms.append(formFollow)

    userFollowsMe = request.user.followed_by.all()

    return render(request, "authentication/abonnements.html", context={
        "userFollowsAdd_forms": userFollowsAdd_forms,
        "userFollowsByMe_forms": userFollowsByMe_forms,
        "userFollowsMe": userFollowsMe
    })
