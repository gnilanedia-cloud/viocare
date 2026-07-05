from django.urls import path

from . import views

app_name = 'consultations'

urlpatterns = [
    path('rejoindre/<int:rdv_id>/', views.rejoindre_consultation, name='rejoindre'),
    path('<int:consultation_id>/terminer/', views.terminer_consultation, name='terminer'),
]
