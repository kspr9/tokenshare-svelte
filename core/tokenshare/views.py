from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class AuthSpaView(LoginRequiredMixin, TemplateView):
    template_name = "tokenshare/index.html"

class NoAuthSpaView(TemplateView):
    template_name = "tokenshare/index.html"