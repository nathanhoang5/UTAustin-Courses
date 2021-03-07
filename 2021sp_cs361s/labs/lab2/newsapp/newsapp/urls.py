"""newsapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import time
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from django import forms
from newslister.models import UserXtraAuth
from newslister.views import register_view, account
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def getToken(seed, refresh=30, salt=b"", info=b"fake-rsa-token"):

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=3,
        salt=salt,
        info=info,
    )
    token_time = time.time()
    cur_epoch = int(token_time / refresh)
    next_time = (cur_epoch + 1) * refresh
    return int.from_bytes(hkdf.derive(seed + cur_epoch.to_bytes(4, "big")), "big")


class TokenLoginForm(AuthenticationForm):
    def clean(self):
        # STUDENT TODO:
        # This is where password processing takes place.
        # For 2-factor authentication, you need to
        # check that the token number is appended to
        # the end of the password entered by the user
        # You don't need to check the password; Django is
        # doing that.
        user_secrecy = 0
        token_seed = b""
        if UserXtraAuth.objects.filter(username=self.cleaned_data["username"]).exists():
            user_xtra_auth = UserXtraAuth.objects.get(
                username=self.cleaned_data["username"]
            )
            user_secrecy = user_xtra_auth.secrecy
            token_seed = user_xtra_auth.tokenkey.encode()
        if user_secrecy > 0:
            pw = self.cleaned_data["password"]
            token = str(getToken(token_seed))
            if len(pw) < len(token) or pw[-len(token) :] != token:
                raise ValidationError("Invalid Token Code")
            self.cleaned_data["password"] = pw[: -len(token)]

        # the password in the form in self._cleaned_data['password']
        return super().clean()


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html", authentication_form=TokenLoginForm
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path("register/", register_view, name="register"),
    path("admin/", admin.site.urls),
    # This line will look for urls in app
    path("", include("newslister.urls")),
    path("newslist/", include("newslister.urls")),
    path("account/", account, name="account"),
]
