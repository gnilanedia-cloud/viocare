from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from appointments.models import RendezVous

from .models import Consultation


@login_required
def rejoindre_consultation(request, rdv_id):
    rdv = get_object_or_404(RendezVous, id=rdv_id)

    if request.user not in (rdv.patient, rdv.medecin):
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette consultation.")
        return redirect('accounts:dashboard')

    if rdv.statut != RendezVous.Statut.CONFIRME:
        messages.warning(request, "Ce rendez-vous n'est pas encore confirmé.")
        return redirect('appointments:mes_rendez_vous')

    consultation, cree = Consultation.objects.get_or_create(rendez_vous=rdv)
    if not consultation.demarree_le:
        consultation.demarree_le = timezone.now()
        consultation.save(update_fields=['demarree_le'])

    display_name = request.user.get_full_name() or request.user.username

    return render(request, 'consultations/salle.html', {
        'consultation': consultation,
        'rdv': rdv,
        'jitsi_domain': settings.JITSI_DOMAIN,
        'display_name': display_name,
        'est_medecin': request.user == rdv.medecin,
    })


@login_required
def terminer_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    if request.user != consultation.rendez_vous.medecin:
        messages.error(request, "Seul le médecin peut clôturer la consultation.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        consultation.notes_medecin = request.POST.get('notes_medecin', '')
        consultation.terminee_le = timezone.now()
        consultation.save()
        consultation.rendez_vous.statut = RendezVous.Statut.TERMINE
        consultation.rendez_vous.save(update_fields=['statut'])
        messages.success(request, "Consultation clôturée et notes enregistrées.")
        return redirect('appointments:agenda_medecin')

    return render(request, 'consultations/terminer.html', {'consultation': consultation})
