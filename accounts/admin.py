from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'specialite', 'telephone')
    list_filter = ('role', 'specialite')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialite')
