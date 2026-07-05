from django.conf import settings
from django.db import models


class DossierMedical(models.Model):
    """Dossier médical central d'un patient."""

    GROUPES_SANGUINS = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
        ('inconnu', 'Inconnu'),
    ]

    patient = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dossier_medical'
    )
    groupe_sanguin = models.CharField(max_length=10, choices=GROUPES_SANGUINS, default='inconnu')
    allergies = models.TextField(blank=True, help_text="Allergies connues (une par ligne)")
    antecedents_medicaux = models.TextField(blank=True, help_text="Antécédents médicaux et chirurgicaux")
    traitements_en_cours = models.TextField(blank=True)
    contact_urgence_nom = models.CharField(max_length=150, blank=True)
    contact_urgence_telephone = models.CharField(max_length=20, blank=True)
    mis_a_jour_le = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Dossier médical'
        verbose_name_plural = 'Dossiers médicaux'

    def __str__(self):
        return f"Dossier médical de {self.patient.get_full_name() or self.patient.username}"


class DocumentMedical(models.Model):
    """Document/pièce jointe versée au dossier médical (résultats d'analyses, imagerie...)."""

    dossier = models.ForeignKey(DossierMedical, on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=150)
    fichier = models.FileField(upload_to='documents_medicaux/%Y/%m/')
    ajoute_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    ajoute_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ajoute_le']

    def __str__(self):
        return self.titre
