from django import template
from django.shortcuts import get_object_or_404
from authentication.models import User

register = template.Library()

@register.simple_tag()
def get_user_follow_display(user_id):
    user = get_object_or_404(User, id=user_id)
    return user.username