from django.views.generic import TemplateView

class SiteTemplateView(TemplateView):
    template_name = 'event_site/index.html'
