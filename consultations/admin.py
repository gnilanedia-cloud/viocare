from django.contrib import admin

from .models import Consultation


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('nom_salle', 'rendez_vous', 'demarree_le', 'terminee_le')
    search_fields = ('nom_salle',)
