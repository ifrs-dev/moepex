from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from event_site.forms import SignUpForm
from events.models import Event, Experiment


class HomeView(ListView):
    model = Event
    template_name = 'event_site/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['experiments'] = Experiment.objects.filter(status=2)
        context['events'] = Event.objects.filter(status=2)
        context['users'] = User.objects.all()
        return context


class PresentationTemplateView(TemplateView):
    template_name = 'event_site/presentation.html'


class SignUpView (CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })