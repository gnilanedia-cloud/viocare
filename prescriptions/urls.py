from django.urls import path

from . import views

app_name = 'prescriptions'

urlpatterns = [
    path('creer/<int:consultation_id>/', views.creer_prescription, name='creer'),
    path('mes-ordonnances/', views.mes_prescriptions, name='liste'),
    path('<int:prescription_id>/', views.detail_prescription, name='detail'),
]
