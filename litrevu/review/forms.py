from django import forms

from review.models import Ticket, Review

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        # fields = '__all__'
        exclude = ("user",)
        widgets = {
            # On force l'utilisation du widget simple sans case à cocher
            "image": forms.FileInput(),
            "description": forms.Textarea(attrs={
                'rows': 5,
                'cols': 40
            })
        }


class ReviewForm(forms.ModelForm):
    # Normalement devrait supprimer les : des noms de champs mais cela ce fonctionne pas
    label_suffix = ""

    class Meta:
        model = Review
        fields = ["headline", "rating", "body",]
        labels = {
            "rating": "Note",
            "headline": "Titre",
            "body": "Commentaire"
        }
        widgets = {
            "rating": forms.RadioSelect(),
            "body": forms.Textarea(attrs={
                'rows': 5,
                'cols': 40
            })
        }