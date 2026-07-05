from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from .forms import InscriptionPatientForm, InscriptionMedecinForm, ProfileForm
from .models import Profile


def choix_inscription(request):
    """Page permettant de choisir : je suis patient ou médecin."""
    return render(request, 'accounts/choix_inscription.html')


def inscription_patient(request):
    if request.method == 'POST':
        form = InscriptionPatientForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bienvenue sur VisioCare ! Votre compte patient a été créé.")
            return redirect('accounts:dashboard')
    else:
        form = InscriptionPatientForm()
    return render(request, 'accounts/inscription_patient.html', {'form': form})


def inscription_medecin(request):
    if request.method == 'POST':
        form = InscriptionMedecinForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Bienvenue sur VisioCare ! Votre compte médecin a été créé.")
            return redirect('accounts:dashboard')
    else:
        form = InscriptionMedecinForm()
    return render(request, 'accounts/inscription_medecin.html', {'form': form})


@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.is_medecin:
        return redirect('appointments:agenda_medecin')
    return redirect('appointments:mes_rendez_vous')


@login_required
def modifier_profil(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour.")
            return redirect('accounts:profil')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/modifier_profil.html', {'form': form})


@login_required
def voir_profil(request):
    return render(request, 'accounts/profil.html', {'profile': request.user.profile})


def liste_medecins(request):
    """Annuaire public des médecins disponibles pour prise de rendez-vous."""
    medecins = Profile.objects.filter(role=Profile.Role.MEDECIN).select_related('user')
    specialite = request.GET.get('specialite', '')
    if specialite:
        medecins = medecins.filter(specialite__icontains=specialite)
    specialites = (
        Profile.objects.filter(role=Profile.Role.MEDECIN)
        .exclude(specialite='')
        .values_list('specialite', flat=True)
        .distinct()
    )
    return render(request, 'accounts/liste_medecins.html', {
        'medecins': medecins,
        'specialites': specialites,
        'specialite_active': specialite,
    })


def fiche_medecin(request, medecin_id):
    profile = get_object_or_404(Profile, id=medecin_id, role=Profile.Role.MEDECIN)
    return render(request, 'accounts/fiche_medecin.html', {'medecin': profile})
