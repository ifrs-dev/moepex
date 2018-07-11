from django.contrib import admin
from django.urls import path

from event_site import views

urlpatterns = [
    path('', views.SiteTemplateView.as_view()),
    path('admin/', admin.site.urls),
]
