from django.contrib import admin
from django.urls import path

import review.views
import authentication.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", review.views.Home.as_view(), name="home"),
    path("", review.views.Base.as_view()),
    path("sign-up", authentication.views.SignUp.as_view(), name="sign_up"),
    path("login", authentication.views.LoginPage.as_view(), name="login"),
    path("logout", authentication.views.logout_user, name="logout"),
]
