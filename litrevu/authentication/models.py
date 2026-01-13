from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """Custom user template."""

    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'Créateur'),
        (SUBSCRIBER, 'Abonné'),
    )

    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    follows = models.ManyToManyField(
        'self',
        through='UserFollows',
        symmetrical=False,
        related_name='followers'
    )

# user.follows.all() (renvoie les gens que je suis)
# user.followers.all() renvoie ceux qui me suivent
# user.following.all() (renvoi des objets UserFollows)


class UserFollows(models.Model):
    """Template for managing user tracking.

    Args:
        models : Base class for creating models.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        # Empêche de suivre deux fois la même personne
        unique_together = ('user', 'followed_user')
