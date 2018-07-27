from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from event_site import views as views_event_site
from events import views as views_events

urlpatterns = [
    path('', views_event_site.SiteTemplateView.as_view(), name='home'),
    path('eventos/novo', views_events.EventCreateView.as_view(), name='event-create'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
