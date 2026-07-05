import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import PriseRendezVousForm, DisponibiliteForm
from .models import RendezVous, Disponibilite


def _creneaux_disponibles(medecin, date):
    """Calcule les créneaux libres d'un médecin pour une date donnée."""
    jour_semaine = date.weekday()
    disponibilites = Disponibilite.objects.filter(medecin=medecin, jour_semaine=jour_semaine)
    creneaux = []
    for dispo in disponibilites:
        courant = datetime.datetime.combine(date, dispo.heure_debut)
        fin = datetime.datetime.combine(date, dispo.heure_fin)
        pas = datetime.timedelta(minutes=dispo.duree_creneau_minutes)
        while courant + pas <= fin:
            creneaux.append(courant.time())
            courant += pas

    deja_pris = set(
        RendezVous.objects.filter(
            medecin=medecin, date=date
        ).exclude(statut=RendezVous.Statut.ANNULE).values_list('heure', flat=True)
    )
    return sorted(c for c in creneaux if c not in deja_pris)


@login_required
def prendre_rendez_vous(request, medecin_id):
    medecin = get_object_or_404(User, id=medecin_id, profile__role='medecin')
    if not request.user.profile.is_patient:
        messages.error(request, "Seuls les patients peuvent prendre rendez-vous.")
        return redirect('accounts:liste_medecins')

    date_choisie = request.GET.get('date') or request.POST.get('date')
    creneaux = []
    if date_choisie:
        try:
            date_obj = datetime.datetime.strptime(date_choisie, '%Y-%m-%d').date()
            creneaux = _creneaux_disponibles(medecin, date_obj)
        except ValueError:
            date_obj = None
    else:
        date_obj = None

    if request.method == 'POST':
        form = PriseRendezVousForm(request.POST, creneaux_disponibles=creneaux)
        if form.is_valid():
            heure_obj = datetime.datetime.strptime(form.cleaned_data['heure'], '%H:%M').time()
            rdv = RendezVous.objects.create(
                patient=request.user,
                medecin=medecin,
                date=date_obj,
                heure=heure_obj,
                motif=form.cleaned_data['motif'],
                statut=RendezVous.Statut.EN_ATTENTE,
            )
            messages.success(request, "Votre demande de rendez-vous a été envoyée au médecin.")
            return redirect('appointments:mes_rendez_vous')
    else:
        form = PriseRendezVousForm(creneaux_disponibles=creneaux)

    return render(request, 'appointments/prendre_rendez_vous.html', {
        'medecin': medecin,
        'form': form,
        'date_choisie': date_choisie,
        'creneaux': creneaux,
    })


@login_required
def mes_rendez_vous(request):
    rdvs = RendezVous.objects.filter(patient=request.user).select_related('medecin__profile')
    return render(request, 'appointments/mes_rendez_vous.html', {'rendez_vous': rdvs})


@login_required
def agenda_medecin(request):
    if not request.user.profile.is_medecin:
        return redirect('appointments:mes_rendez_vous')
    aujourd_hui = timezone.localdate()
    rdvs = RendezVous.objects.filter(
        medecin=request.user, date__gte=aujourd_hui
    ).exclude(statut=RendezVous.Statut.ANNULE).select_related('patient__profile')
    disponibilites = Disponibilite.objects.filter(medecin=request.user)
    return render(request, 'appointments/agenda_medecin.html', {
        'rendez_vous': rdvs,
        'disponibilites': disponibilites,
    })


@login_required
def gerer_disponibilites(request):
    if not request.user.profile.is_medecin:
        return redirect('appointments:mes_rendez_vous')
    if request.method == 'POST':
        form = DisponibiliteForm(request.POST)
        if form.is_valid():
            dispo = form.save(commit=False)
            dispo.medecin = request.user
            dispo.save()
            messages.success(request, "Disponibilité ajoutée à votre agenda.")
            return redirect('appointments:gerer_disponibilites')
    else:
        form = DisponibiliteForm()
    disponibilites = Disponibilite.objects.filter(medecin=request.user)
    return render(request, 'appointments/gerer_disponibilites.html', {
        'form': form,
        'disponibilites': disponibilites,
    })


@login_required
def supprimer_disponibilite(request, dispo_id):
    dispo = get_object_or_404(Disponibilite, id=dispo_id, medecin=request.user)
    dispo.delete()
    messages.success(request, "Disponibilité supprimée.")
    return redirect('appointments:gerer_disponibilites')


@login_required
def confirmer_rendez_vous(request, rdv_id):
    rdv = get_object_or_404(RendezVous, id=rdv_id, medecin=request.user)
    rdv.statut = RendezVous.Statut.CONFIRME
    rdv.save()
    messages.success(request, "Rendez-vous confirmé. Le patient sera notifié.")
    return redirect('appointments:agenda_medecin')


@login_required
def annuler_rendez_vous(request, rdv_id):
    rdv = get_object_or_404(RendezVous, id=rdv_id)
    if request.user not in (rdv.patient, rdv.medecin):
        messages.error(request, "Vous n'êtes pas autorisé à annuler ce rendez-vous.")
    else:
        rdv.statut = RendezVous.Statut.ANNULE
        rdv.save()
        messages.success(request, "Rendez-vous annulé.")
    if request.user.profile.is_medecin:
        return redirect('appointments:agenda_medecin')
    return redirect('appointments:mes_rendez_vous')
