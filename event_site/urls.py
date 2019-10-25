
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include

from event_site import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('usuarios/', include('django.contrib.auth.urls')),
    path('importar/sia/', staff_member_required(views.SiaImporterView.as_view()), name='sia-importer'),
    path('importar/sigaa/', staff_member_required(views.SigaaImporterView.as_view()), name='sigaa-importer'),
    path('importar/servidores/', staff_member_required(views.ServImporterView.as_view()), name='serv-importer'),
    path('certificados/', staff_member_required(views.get_certifieds), name='get-certifieds'),
]
