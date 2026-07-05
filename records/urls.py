from django.urls import path

from . import views

app_name = 'records'

urlpatterns = [
    path('', views.mon_dossier, name='mon_dossier'),
    path('document/ajouter/', views.ajouter_document, name='ajouter_document'),
    path('patient/<int:patient_id>/', views.consulter_dossier_patient, name='dossier_patient'),
]
