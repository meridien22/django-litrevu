from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from authentication.models import UserFollows
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class UserFollowerToAddForm(forms.ModelForm):
    add_follower = forms.BooleanField(widget=forms.HiddenInput, initial=True)
   
    class Meta:
        model = UserFollows
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        # On récupère l'utilisateur passé depuis la vue et on la supprime de kwargs
        # "None" est la valeur par défaut si la clé "user" n'existe pas
        user = kwargs.pop('user', None)
        super(UserFollowerToAddForm, self).__init__(*args, **kwargs)
        
        if user:
            # On filtre pour exclure l'utilisateur actuellement connecté
            # On filtre aussi pour exlure les utilisateurs déjà suivis
            # values_list permet de nesélectionner que la colonne followed_user_id
            # flat=True permet d'avoir une liste à la place d'une liste de tuple

            # On peut obtenir les id des utilisateurs suivis de 2 manières :

            # A partir des followed_user_id des objets UserFollows
            # already_following = user.following.values_list('followed_user_id', flat=True)

            # A partir des id des objets User
            already_following = user.follows.all().values_list('id', flat=True)

            self.fields['followed_user'].queryset = User.objects.exclude(
                id__in=[user.id] + list(already_following)
            )

class UserFollowersForm(forms.ModelForm):
    delete_follower = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = UserFollows
        exclude = ("user",)
        widgets = {
            # Le champ sera présent mais ne sera pas affiché
            # Permet de récupérer 
            "followed_user": forms.HiddenInput(),
            "user": forms.HiddenInput()
        }