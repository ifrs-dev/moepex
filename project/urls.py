from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from event_site import views as views_event_site
from events import views as views_events


urlpatterns = [
    path('', views_events.EventListView.as_view(), name='home'),
    path('eventos/novo', views_events.EventCreateView.as_view(), name='event-create'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
	path('logout/', auth_views.logout, {'next_page': '/login/'}, name="logout"),
    path('evento/<int:pk>/', views_events.EventDetailView.as_view(), name='event-detail'),
    path('eventos/emavaliacao/', views_events.EventInAvaliation.as_view(), name="event-inavaliation"),
    path('eventos/aprovados/', views_events.EventApproved.as_view(), name="event-approved"),
    path('eventos/emcorrecao/', views_events.EventInCorrections.as_view(), name="event-incorrections"),
    path('eventos/negados/', views_events.EventNoApproved.as_view(), name="event-noapproved"),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
