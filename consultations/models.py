import uuid

from django.db import models

from appointments.models import RendezVous


class Consultation(models.Model):
    """Salle de consultation vidéo liée à un rendez-vous confirmé."""

    rendez_vous = models.OneToOneField(
        RendezVous, on_delete=models.CASCADE, related_name='consultation'
    )
    nom_salle = models.CharField(max_length=100, unique=True, editable=False)
    demarree_le = models.DateTimeField(null=True, blank=True)
    terminee_le = models.DateTimeField(null=True, blank=True)
    notes_medecin = models.TextField(
        blank=True, help_text="Notes cliniques rédigées pendant/après la consultation"
    )

    class Meta:
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'

    def save(self, *args, **kwargs):
        if not self.nom_salle:
            self.nom_salle = f"visiocare-{uuid.uuid4().hex[:12]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Consultation - {self.rendez_vous}"

    @property
    def est_terminee(self):
        return self.terminee_le is not None
