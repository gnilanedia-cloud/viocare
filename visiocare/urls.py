"""URLs racine du projet VisioCare."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('comptes/', include('accounts.urls')),
    path('rendez-vous/', include('appointments.urls')),
    path('consultations/', include('consultations.urls')),
    path('ordonnances/', include('prescriptions.urls')),
    path('dossier/', include('records.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
