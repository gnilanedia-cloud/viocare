from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from consultations.models import Consultation

from .forms import PrescriptionForm
from .models import Prescription


@login_required
def creer_prescription(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    if request.user != consultation.rendez_vous.medecin:
        messages.error(request, "Seul le médecin peut rédiger une ordonnance.")
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.consultation = consultation
            prescription.patient = consultation.rendez_vous.patient
            prescription.medecin = request.user
            prescription.save()
            messages.success(request, "Ordonnance créée et ajoutée au dossier du patient.")
            return redirect('prescriptions:detail', prescription_id=prescription.id)
    else:
        form = PrescriptionForm()

    return render(request, 'prescriptions/creer.html', {'form': form, 'consultation': consultation})


@login_required
def mes_prescriptions(request):
    if request.user.profile.is_medecin:
        prescriptions = Prescription.objects.filter(medecin=request.user)
    else:
        prescriptions = Prescription.objects.filter(patient=request.user)
    return render(request, 'prescriptions/liste.html', {'prescriptions': prescriptions})


@login_required
def detail_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    if request.user not in (prescription.patient, prescription.medecin):
        messages.error(request, "Accès non autorisé à cette ordonnance.")
        return redirect('accounts:dashboard')
    return render(request, 'prescriptions/detail.html', {'prescription': prescription})
