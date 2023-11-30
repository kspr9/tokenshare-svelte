from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings


class AuthSpaView(LoginRequiredMixin, TemplateView):
    template_name = "tokenshare/index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in DEBUG
        context['DEBUG'] = settings.DEBUG
        return context

class NoAuthSpaView(TemplateView):
    template_name = "tokenshare/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['DEBUG'] = settings.DEBUG
        return context