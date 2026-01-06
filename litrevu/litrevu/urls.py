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
    path("sign-up", authentication.views.SignUp.as_view(), name="sign_up"),
    path("login", authentication.views.LoginPage.as_view(), name="login"),
    path("logout", authentication.views.logout_user, name="logout"),
    path("tickets/add", review.views.ticket_create, name="ticket_create"),
    path("posts", review.views.posts, name="posts"),
    path("tickets/<int:id>/update/", review.views.ticket_update, name="ticket_update")
]

# modèles d’URL pour que les média mis en ligne soit accessible par le biais d’une URL
# Cette méthode n’est adaptée que dans un environnement de développement.
# Sur un site en production, paramétrez  settings.DEBUGsurFalse
# et implémentez un processus de stockage des médias plus sophistiqué.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)