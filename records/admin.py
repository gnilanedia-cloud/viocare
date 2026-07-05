from django.contrib import admin

from .models import DossierMedical, DocumentMedical


class DocumentInline(admin.TabularInline):
    model = DocumentMedical
    extra = 0


@admin.register(DossierMedical)
class DossierMedicalAdmin(admin.ModelAdmin):
    list_display = ('patient', 'groupe_sanguin', 'mis_a_jour_le')
    inlines = [DocumentInline]
