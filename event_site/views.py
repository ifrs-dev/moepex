from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from event_site.forms import SignUpForm

class SiteTemplateView(TemplateView):
    template_name = 'event_site/index.html'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(),
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})