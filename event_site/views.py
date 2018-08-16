from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from event_site.forms import SignUpForm


class PresentationTemplateView(TemplateView):
    template_name = 'event_site/presentation.html'


class SignUpView (CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
