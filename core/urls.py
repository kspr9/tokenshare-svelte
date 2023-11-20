"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include


from core.tokenshare.views import AuthSpaView, NoAuthSpaView
from core.api.views import GreetingApi, LoginAPIView, AuthUserApi, check_authentication_status

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/greet", GreetingApi.as_view()),
    path('api/check-auth/', check_authentication_status, name='check-auth'),
    path("api/auth-user", AuthUserApi.as_view()),
    path('api/login', LoginAPIView.as_view(), name='api_login'),
    path("app/dashboard", AuthSpaView.as_view(), name="tokenshare"),
    path('', NoAuthSpaView.as_view(), name='home'),
]
