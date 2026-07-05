from django.conf import settings
from django.db import models


JOURS_SEMAINE = [
    (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), (3, 'Jeudi'),
    (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche'),
]


class Disponibilite(models.Model):
    """Créneaux récurrents pendant lesquels un médecin est disponible (agenda)."""

    medecin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='disponibilites', limit_choices_to={'profile__role': 'medecin'}
    )
    jour_semaine = models.IntegerField(choices=JOURS_SEMAINE)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree_creneau_minutes = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ['jour_semaine', 'heure_debut']
        verbose_name = 'Disponibilité'
        verbose_name_plural = 'Disponibilités'

    def __str__(self):
        return f"{self.medecin.get_full_name()} - {self.get_jour_semaine_display()} {self.heure_debut}-{self.heure_fin}"


class RendezVous(models.Model):
    """Rendez-vous pris par un patient auprès d'un médecin."""

    class Statut(models.TextChoices):
        EN_ATTENTE = 'en_attente', 'En attente de confirmation'
        CONFIRME = 'confirme', 'Confirmé'
        TERMINE = 'termine', 'Terminé'
        ANNULE = 'annule', 'Annulé'

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='rendez_vous_patient', limit_choices_to={'profile__role': 'patient'}
    )
    medecin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='rendez_vous_medecin', limit_choices_to={'profile__role': 'medecin'}
    )
    date = models.DateField()
    heure = models.TimeField()
    motif = models.CharField(max_length=255, blank=True)
    statut = models.CharField(max_length=15, choices=Statut.choices, default=Statut.EN_ATTENTE)
    rappel_envoye = models.BooleanField(default=False)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-heure']
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'
        constraints = [
            models.UniqueConstraint(
                fields=['medecin', 'date', 'heure'],
                name='un_seul_rdv_par_creneau_medecin',
            )
        ]

    def __str__(self):
        return f"RDV {self.patient} avec {self.medecin} le {self.date} à {self.heure}"

    @property
    def est_passe(self):
        from django.utils import timezone
        import datetime
        dt = timezone.make_aware(datetime.datetime.combine(self.date, self.heure))
        return dt < timezone.now()
