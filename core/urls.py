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

## API endpoint for testing
from core.api.views import GreetingApi


# Main SPA views / entrypoints to the App
from core.tokenshare.views import AuthSpaView, NoAuthSpaView

# USER AUTH API views / endpoints
from core.api.auth_user_views import LoginAPIView, AuthUserApi, RegisterAPIView, check_authentication_status

# API Views/endpoints for GOVERNANCE model classes
from core.api.governance_views import WorkspaceViewSet, CompanyViewSet, GovernanceContractViewSet, CreateWorkspaceViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/workspaces', WorkspaceViewSet)
router.register(r'api/companies', CompanyViewSet)
router.register(r'api/contracts', GovernanceContractViewSet)
router.register(r'api/create_workspace', CreateWorkspaceViewSet, basename='create_workspace')


urlpatterns = [
    path("admin/", admin.site.urls),
    #path("accounts/", include("django.contrib.auth.urls")),

    # API endpoints for managing user authentication
    path('api/check-auth/', check_authentication_status, name='check-auth'),
    path("api/auth-user", AuthUserApi.as_view()),
    path('api/login', LoginAPIView.as_view(), name='api_login'),
    path('api/register', RegisterAPIView.as_view(), name='api_register'),
    
    # Main SPA views - 1) authenticated views, 2) unauthenticated views
    path("app/dashboard", AuthSpaView.as_view(), name="tokenshare"),
    path('', NoAuthSpaView.as_view(), name='home'),

    # messaging/user communications
    path('user_comms/', include('core.userComms.urls')),

    # can be deleted at some point, just for testing
    path("api/greet", GreetingApi.as_view()),
] + router.urls
