from datetime import date

from easy_pdf.views import PDFTemplateResponseMixin
from django.views.generic.edit import CreateView
from django.views.generic import View, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv

from events.models import Event, Registration, Group, Experiment, CHOICES_SHIFTS_2, CHOICES_SHIFTS_4
from events.forms import EventForm, ExperimentForm, GroupForm


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy('group-list', args=(self.object.id,))

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.pk
        return initial

class ExperimentCreateView(CreateView):
    model = Experiment
    template_name = 'events/event-create.html'
    form_class = ExperimentForm
    success_url = reverse_lazy('my-events')

    def get_initial(self):
        initial = super().get_initial()
        initial['author'] = self.request.user.pk
        return initial


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        context['groups'] = Group.objects.filter(event=self.get_object())

        if not user.is_authenticated:
            context['registred'] = 'not_user'
        else:
            try:
                events = Registration.objects.filter(group__event=self.get_object(), user=user)
                if events.exists():
                    context['registred'] = 'valid'
            except:
                pass
            if user == self.get_object().author:
                context['author'] = True
            else:
                context['author'] = False
        return context


class ExperimentDetailView(DetailView):
    model = Experiment
    template_name = 'experiments/experiment-detail.html'


class EventRegistrationView(DetailView):
    model = Group

    def get(self, request, *args, **kwargs):
        Registration.objects.create(group=self.get_object(), user=request.user)
        return redirect('event-detail', self.get_object().event.pk)


class MyRegistrationsListView(ListView):
    model = Registration
    template_name = 'events/my-events.html'


class GroupListView(DetailView):
    model = Event
    template_name = 'groups/group-list.html'


class GroupCreateView(DetailView, CreateView):
    model = Event
    template_name = 'groups/group-create.html'
    form_class = GroupForm

    def get_success_url(self):
        return reverse_lazy('group-list', args=(self.get_object().id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        event = self.get_object()
        EXCLUDE = [(e.shift, e.get_shift_display()) for e in event.groups.all()]
        if event.workload == 1:
            kwargs['choices'] = set(CHOICES_SHIFTS_2) - set(EXCLUDE)
        else:
            kwargs['choices'] = set(CHOICES_SHIFTS_4) - set(EXCLUDE)
        return kwargs

    def get(self, request, *args, **kwargs):
        if self.request.user == self.get_object().author:
            return super().get(request, *args, **kwargs)
        return redirect('event-detail', self.get_object().event.pk)

    def form_valid(self, form):
        form.instance.event = self.get_object()
        return super().form_valid(form)


class RegistrationUpdateView(DetailView):
    model = Registration
    status = 1

    def get(self, request, *args, **kwargs):
        registration = self.get_object()
        registration.status = self.status
        registration.save()
        return redirect('registrations-list', registration.group.id)


class RegistrationPresentView(RegistrationUpdateView):
    status = 2


class RegistrationAbsentView(RegistrationUpdateView):
    status = 3


class RegistrationsListView(DetailView):
    model = Group
    template_name = "events/registrations-list.html"
    pdf = False

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        event = self.get_object()
        context['registrations'] = Registration.objects.filter(group=self.get_object()).order_by('user__first_name')
        context['pdf'] = self.pdf
        return context

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.POST['cpf'])
        registration = Registration.objects.get(user=user, group=self.get_object())
        registration.status = 2
        registration.save()
        return super().get(request, *args, **kwargs)

class RegistrationsPDFView(RegistrationsListView, PDFTemplateResponseMixin):
    template_name = 'events/registrations-list-pdf.html'
    pdf = True

class RegistrationDetailView(DetailView, PDFTemplateResponseMixin):
    model = Registration
    template_name = "registrations-detail-pdf.html"
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000


def getfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inscritos.csv"'
    r = Registration.objects.all()
    writer = csv.writer(response)
    for r in registrations:
        writer.writerow([registrations.user.get_full_name, registrations.get_status_display])
    return response