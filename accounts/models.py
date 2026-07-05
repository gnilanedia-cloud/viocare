from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Extension du User Django avec un rôle (patient ou médecin)."""

    class Role(models.TextChoices):
        PATIENT = 'patient', 'Patient'
        MEDECIN = 'medecin', 'Médecin'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.PATIENT)
    telephone = models.CharField(max_length=20, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='profils/', blank=True, null=True)

    # Champs spécifiques aux médecins
    specialite = models.CharField(max_length=100, blank=True)
    numero_ordre = models.CharField(
        max_length=50, blank=True,
        help_text="Numéro d'inscription à l'ordre des médecins"
    )
    biographie = models.TextField(blank=True)
    tarif_consultation = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def is_medecin(self):
        return self.role == self.Role.MEDECIN

    @property
    def is_patient(self):
        return self.role == self.Role.PATIENT
