from django import forms

from review.models import Ticket, Review


class TicketForm(forms.ModelForm):
    """Form for submitting an existing ticket or creating a new ticket.

    Args:
        forms : Base class for creating forms.
    """
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
    """Form allowing you to submit an existing review or create a new review.

    Args:
        forms : Base class for creating forms.
    """
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
