from django.urls import path

from . import views

app_name = 'appointments'

urlpatterns = [
    path('prendre/<int:medecin_id>/', views.prendre_rendez_vous, name='prendre_rendez_vous'),
    path('mes-rendez-vous/', views.mes_rendez_vous, name='mes_rendez_vous'),
    path('agenda/', views.agenda_medecin, name='agenda_medecin'),
    path('disponibilites/', views.gerer_disponibilites, name='gerer_disponibilites'),
    path('disponibilites/<int:dispo_id>/supprimer/', views.supprimer_disponibilite, name='supprimer_disponibilite'),
    path('<int:rdv_id>/confirmer/', views.confirmer_rendez_vous, name='confirmer_rendez_vous'),
    path('<int:rdv_id>/annuler/', views.annuler_rendez_vous, name='annuler_rendez_vous'),
]
