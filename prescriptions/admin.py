from django.contrib import admin

from .models import Prescription


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date_emission', 'valide_jusquau')
    search_fields = ('patient__username', 'medecin__username')
