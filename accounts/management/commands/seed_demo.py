"""
Crée des comptes de démonstration (1 médecin, 1 patient) avec des
disponibilités, pour tester rapidement l'application.

Usage : python manage.py seed_demo
"""
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import Profile
from appointments.models import Disponibilite


class Command(BaseCommand):
    help = "Crée des comptes de démonstration (médecin + patient)."

    def handle(self, *args, **options):
        if not User.objects.filter(username='dr.diop').exists():
            medecin = User.objects.create_user(
                username='dr.diop', password='VisioCare2026!',
                first_name='Awa', last_name='Diop', email='dr.diop@example.com'
            )
            medecin.profile.role = Profile.Role.MEDECIN
            medecin.profile.specialite = 'Médecine générale'
            medecin.profile.numero_ordre = 'SN-00123'
            medecin.profile.biographie = "10 ans d'expérience en médecine générale et téléconsultation."
            medecin.profile.tarif_consultation = 15000
            medecin.profile.save()

            for jour in range(0, 5):  # du lundi au vendredi
                Disponibilite.objects.create(
                    medecin=medecin, jour_semaine=jour,
                    heure_debut=datetime.time(9, 0), heure_fin=datetime.time(12, 0),
                    duree_creneau_minutes=30,
                )
            self.stdout.write(self.style.SUCCESS("Médecin de démo créé : dr.diop / VisioCare2026!"))
        else:
            self.stdout.write("Le médecin de démo existe déjà.")

        if not User.objects.filter(username='patient.demo').exists():
            patient = User.objects.create_user(
                username='patient.demo', password='VisioCare2026!',
                first_name='Moussa', last_name='Fall', email='patient.demo@example.com'
            )
            patient.profile.role = Profile.Role.PATIENT
            patient.profile.save()
            self.stdout.write(self.style.SUCCESS("Patient de démo créé : patient.demo / VisioCare2026!"))
        else:
            self.stdout.write("Le patient de démo existe déjà.")
