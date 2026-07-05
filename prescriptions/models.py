from django.conf import settings
from django.db import models

from consultations.models import Consultation


class Prescription(models.Model):
    """Ordonnance numérique délivrée par un médecin à l'issue d'une consultation."""

    consultation = models.ForeignKey(
        Consultation, on_delete=models.CASCADE, related_name='prescriptions'
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescriptions'
    )
    medecin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescriptions_redigees'
    )
    medicaments = models.TextField(
        help_text="Un médicament par ligne, avec posologie (ex : Paracétamol 500mg - 1 cp x3/jour pendant 5 jours)"
    )
    instructions = models.TextField(blank=True, help_text="Recommandations complémentaires")
    date_emission = models.DateTimeField(auto_now_add=True)
    valide_jusquau = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date_emission']
        verbose_name = 'Ordonnance'
        verbose_name_plural = 'Ordonnances'

    def __str__(self):
        return f"Ordonnance pour {self.patient} du {self.date_emission:%d/%m/%Y}"

    @property
    def liste_medicaments(self):
        return [ligne.strip() for ligne in self.medicaments.splitlines() if ligne.strip()]
