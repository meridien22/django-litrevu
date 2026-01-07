from django import forms

from review.models import Ticket

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
