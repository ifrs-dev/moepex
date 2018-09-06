from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from event_site import views as views_event_site
from events import views as views_events


urlpatterns = [
    path('', views_event_site.HomeView.as_view(), name='home'),
    path('apresentacao', views_event_site.PresentationTemplateView.as_view(), name='presentation'),
    path('programacao', views_event_site.ProgramTemplateView.as_view(), name='program'),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('change_password', views_event_site.change_password, name='change_password'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('cadastro/', views_event_site.SignUpView.as_view(), name='signup'),
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


admin.site.site_header = 'Moepex'
admin.site.site_title = 'Moepex'
