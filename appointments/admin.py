from django.contrib import admin

from .models import RendezVous, Disponibilite


@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date', 'heure', 'statut')
    list_filter = ('statut', 'date')
    search_fields = ('patient__username', 'medecin__username')


@admin.register(Disponibilite)
class DisponibiliteAdmin(admin.ModelAdmin):
    list_display = ('medecin', 'jour_semaine', 'heure_debut', 'heure_fin')
    list_filter = ('jour_semaine',)
