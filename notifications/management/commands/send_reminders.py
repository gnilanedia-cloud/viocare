"""
Commande d'envoi des rappels automatiques de rendez-vous.

Usage :
    python manage.py send_reminders

À planifier en tâche quotidienne (ex : PythonAnywhere > Tasks, ou cron)
pour envoyer un rappel par e-mail aux patients dont le rendez-vous est
prévu le lendemain.
"""
import datetime

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from appointments.models import RendezVous


class Command(BaseCommand):
    help = "Envoie un rappel par e-mail pour les rendez-vous confirmés prévus demain."

    def handle(self, *args, **options):
        demain = timezone.localdate() + datetime.timedelta(days=1)
        rdvs = RendezVous.objects.filter(
            date=demain,
            statut=RendezVous.Statut.CONFIRME,
            rappel_envoye=False,
        ).select_related('patient', 'medecin')

        total = 0
        for rdv in rdvs:
            if not rdv.patient.email:
                continue
            sujet = "Rappel : rendez-vous VisioCare demain"
            message = (
                f"Bonjour {rdv.patient.first_name or rdv.patient.username},\n\n"
                f"Nous vous rappelons votre consultation à distance avec le "
                f"Dr {rdv.medecin.get_full_name() or rdv.medecin.username} "
                f"prévue le {rdv.date.strftime('%d/%m/%Y')} à {rdv.heure.strftime('%H:%M')}.\n\n"
                f"Connectez-vous à votre espace VisioCare pour rejoindre la consultation "
                f"à l'heure prévue.\n\n"
                f"— L'équipe VisioCare"
            )
            send_mail(
                sujet, message, settings.DEFAULT_FROM_EMAIL,
                [rdv.patient.email], fail_silently=True,
            )
            rdv.rappel_envoye = True
            rdv.save(update_fields=['rappel_envoye'])
            total += 1

        self.stdout.write(self.style.SUCCESS(f"{total} rappel(s) envoyé(s)."))
