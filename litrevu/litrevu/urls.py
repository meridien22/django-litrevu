from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import review.views
import authentication.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", review.views.Home.as_view(), name="home"),
    path("", review.views.Base.as_view()),
    path("sign-up/", authentication.views.SignUp.as_view(), name="sign_up"),
    path("login/", authentication.views.LoginPage.as_view(), name="login"),
    path("logout/", authentication.views.logout_user, name="logout"),
    path("posts/", review.views.posts, name="posts"),
    path("flux/", review.views.flux, name="flux"),
    path("tickets/add", review.views.ticket_create, name="ticket_create"),
    path("tickets/<int:id>/update/", review.views.ticket_update, name="ticket_update"),
    path("tickets/<int:id>/delete/", review.views.ticket_delete, name="ticket_delete"),
    path("tickets/<int:id>/review/", review.views.ticket_review, name="ticket_review"),
    path("ticket_review/add", review.views.ticket_review_create, name="ticket_review_create"),
    path("reviews/<int:id>/update/", review.views.review_update, name="review_update"),
    path("reviews/<int:id>/delete/", review.views.review_delete, name="review_delete"),
    path("abonnements/", authentication.views.abonnements, name="abonnements")
]

# modèles d’URL pour que les média mis en ligne soit accessible par le biais d’une URL
# Cette méthode n’est adaptée que dans un environnement de développement.
# Sur un site en production, paramétrez  settings.DEBUGsurFalse
# et implémentez un processus de stockage des médias plus sophistiqué.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)