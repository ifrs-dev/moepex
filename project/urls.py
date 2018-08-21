from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

from event_site import views as views_event_site
from events import views as views_events


urlpatterns = [
    path('', views_events.HomeView.as_view(), name='home'),
    path('apresentacao', views_event_site.PresentationTemplateView.as_view(), name='presentation'),
    path('experimento/<int:pk>/', views_events.ExperimentDetailView.as_view(), name='experiment-detail'),
    path('minicurso/<int:pk>/', views_events.EventDetailView.as_view(), name='event-detail'),
    path('turmas/<int:pk>/', views_events.GroupDetailView.as_view(), name='group-detail'),
    path('turma/novo/', views_events.GroupCreateView.as_view(), name='group-create'),

    path('meus-eventos/', login_required(views_events.MyRegistrationsListView.as_view()), name='my-events'),
    path('experimento/novo/', login_required(views_events.ExperimentCreateView.as_view()), name='experiment-create'),
    path('minicurso/novo/', login_required(views_events.EventCreateView.as_view()), name='event-create'),
    path('minicurso/inscricao/<int:pk>/', login_required(views_events.EventRegistrationView.as_view()), name="event-registration"),

    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/login/'}, name="logout"),
    path('signup/', views_event_site.SignUpView.as_view(), name='signup'),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = 'Moepex'
admin.site.site_title = 'Moepex'
