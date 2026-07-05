from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from appointments.models import RendezVous
from prescriptions.models import Prescription

from .forms import DossierMedicalForm, DocumentMedicalForm
from .models import DossierMedical


@login_required
def mon_dossier(request):
    if not request.user.profile.is_patient:
        messages.error(request, "Cette page est réservée aux patients.")
        return redirect('accounts:dashboard')

    dossier, _ = DossierMedical.objects.get_or_create(patient=request.user)

    if request.method == 'POST':
        form = DossierMedicalForm(request.POST, instance=dossier)
        if form.is_valid():
            form.save()
            messages.success(request, "Dossier médical mis à jour.")
            return redirect('records:mon_dossier')
    else:
        form = DossierMedicalForm(instance=dossier)

    document_form = DocumentMedicalForm()
    historique = RendezVous.objects.filter(
        patient=request.user, statut=RendezVous.Statut.TERMINE
    ).select_related('medecin__profile')
    prescriptions = Prescription.objects.filter(patient=request.user)

    return render(request, 'records/dossier.html', {
        'dossier': dossier,
        'form': form,
        'document_form': document_form,
        'historique': historique,
        'prescriptions': prescriptions,
    })


@login_required
def ajouter_document(request):
    dossier, _ = DossierMedical.objects.get_or_create(patient=request.user)
    if request.method == 'POST':
        form = DocumentMedicalForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.dossier = dossier
            document.ajoute_par = request.user
            document.save()
            messages.success(request, "Document ajouté au dossier médical.")
    return redirect('records:mon_dossier')


@login_required
def consulter_dossier_patient(request, patient_id):
    """Permet à un médecin de consulter le dossier d'un patient qu'il suit."""
    if not request.user.profile.is_medecin:
        messages.error(request, "Accès réservé aux médecins.")
        return redirect('accounts:dashboard')

    patient = get_object_or_404(User, id=patient_id, profile__role='patient')

    a_deja_consulte = RendezVous.objects.filter(
        patient=patient, medecin=request.user
    ).exists()
    if not a_deja_consulte:
        messages.error(request, "Vous n'avez pas de rendez-vous avec ce patient.")
        return redirect('appointments:agenda_medecin')

    dossier = getattr(patient, 'dossier_medical', None)
    historique = RendezVous.objects.filter(
        patient=patient, medecin=request.user, statut=RendezVous.Statut.TERMINE
    )
    prescriptions = Prescription.objects.filter(patient=patient, medecin=request.user)

    return render(request, 'records/dossier_patient.html', {
        'patient': patient,
        'dossier': dossier,
        'historique': historique,
        'prescriptions': prescriptions,
    })
