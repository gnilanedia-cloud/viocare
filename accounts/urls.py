from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.choix_inscription, name='choix_inscription'),
    path('inscription/patient/', views.inscription_patient, name='inscription_patient'),
    path('inscription/medecin/', views.inscription_medecin, name='inscription_medecin'),
    path('connexion/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(), name='logout'),
    path('tableau-de-bord/', views.dashboard, name='dashboard'),
    path('profil/', views.voir_profil, name='profil'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('medecins/', views.liste_medecins, name='liste_medecins'),
    path('medecins/<int:medecin_id>/', views.fiche_medecin, name='fiche_medecin'),

    # Réinitialisation de mot de passe
    path('mot-de-passe/reinitialiser/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),
    path('mot-de-passe/reinitialiser/envoye/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('mot-de-passe/reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('mot-de-passe/reinitialiser/termine/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
