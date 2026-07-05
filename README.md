# VisioCare — Plateforme de télémédecine et consultation à distance

Application Django permettant à des patients de consulter des médecins à
distance par visioconférence sécurisée.

## Fonctionnalités

- Prise de rendez-vous en ligne
- Agenda des médecins (disponibilités récurrentes)
- Consultation vidéo sécurisée (intégration Jitsi Meet, gratuite, sans clé API)
- Ordonnances numériques (imprimables / exportables en PDF via le navigateur)
- Dossier médical sécurisé (allergies, antécédents, documents)
- Historique des consultations
- Rappels automatiques par e-mail (commande planifiable)

## Stack technique

- Python 3.10+ / Django 5
- SQLite (base par défaut, adaptée à PythonAnywhere free tier)
- Bootstrap 5 (interface)
- Jitsi Meet (visioconférence, embarqué en iframe/JS — aucune clé API requise)
- WhiteNoise (fichiers statiques en production)

---

## 1. Installation en local

```bash
git clone https://github.com/VOTRE-UTILISATEUR/visiocare.git
cd visiocare

python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # compte admin
python manage.py seed_demo         # (optionnel) crée un médecin + un patient de démo

python manage.py runserver
```

Rendez-vous sur http://127.0.0.1:8000

Comptes de démo créés par `seed_demo` :
- Médecin : `dr.diop` / `VisioCare2026!`
- Patient : `patient.demo` / `VisioCare2026!`

---

## 2. Déposer le projet sur GitHub

```bash
cd visiocare
git init
git add .
git commit -m "Premier commit - VisioCare"
git branch -M main

# Créez d'abord un dépôt vide sur https://github.com/new (sans README)
git remote add origin https://github.com/VOTRE-UTILISATEUR/visiocare.git
git push -u origin main
```

> Le fichier `.gitignore` exclut déjà `db.sqlite3`, `media/`, `staticfiles/`
> et les environnements virtuels : vous ne poussez que le code source.

---

## 3. Déployer sur PythonAnywhere

### a) Créer un compte et un dépôt

1. Créez un compte sur https://www.pythonanywhere.com
2. Ouvrez une **Bash console** depuis le tableau de bord.
3. Clonez votre dépôt :
   ```bash
   git clone https://github.com/VOTRE-UTILISATEUR/visiocare.git
   ```

### b) Créer l'environnement virtuel et installer les dépendances

```bash
cd visiocare
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### c) Configurer les variables d'environnement

Dans la console Bash, créez un fichier `.env` (ou définissez-les directement
dans le fichier WSGI à l'étape e) :

```bash
export DJANGO_SECRET_KEY="une-cle-secrete-longue-et-aleatoire"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="visiocare.pythonanywhere.com"
export DJANGO_CSRF_TRUSTED_ORIGINS="https://visiocare.pythonanywhere.com"
```

Générez une clé secrète robuste avec :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### d) Préparer la base de données et les fichiers statiques

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### e) Configurer l'application web

1. Onglet **Web** > **Add a new web app** > choisissez **Manual configuration** > Python 3.10.
2. Dans la section **Code** :
   - **Source code** : `/home/visiocare/visiocare`
   - **Working directory** : `/home/visiocare/visiocare`
3. Dans la section **Virtualenv** :
   - `/home/visiocare/visiocare/venv`
4. Cliquez sur le lien **WSGI configuration file** et remplacez son contenu par :

   ```python
   import os
   import sys

   path = '/home/visiocare/visiocare'
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'visiocare.settings'
   os.environ['DJANGO_SECRET_KEY'] = 'une-cle-secrete-longue-et-aleatoire'
   os.environ['DJANGO_DEBUG'] = 'False'
   os.environ['DJANGO_ALLOWED_HOSTS'] = 'visiocare.pythonanywhere.com'
   os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://visiocare.pythonanywhere.com'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

5. Dans la section **Static files**, ajoutez :
   - URL `/static/` → Directory `/home/visiocare/visiocare/staticfiles`
   - URL `/media/` → Directory `/home/visiocare/visiocare/media`

6. Cliquez sur **Reload** en haut de la page.

Votre application est en ligne sur `https://visiocare.pythonanywhere.com`.

### f) Rappels automatiques (tâche planifiée)

Dans l'onglet **Tasks** de PythonAnywhere (disponible même sur le compte
gratuit, 1 tâche par jour), ajoutez une tâche quotidienne :

```bash
source /home/visiocare/visiocare/venv/bin/activate && python /home/visiocare/visiocare/manage.py send_reminders
```

### g) Mettre à jour l'application après un nouveau commit

```bash
cd ~/visiocare
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
# Puis cliquez sur "Reload" dans l'onglet Web de PythonAnywhere
```

---

## Structure du projet

```
visiocare/
├── accounts/        # Comptes patients/médecins, authentification, profils
├── appointments/     # Disponibilités des médecins, prise de rendez-vous
├── consultations/    # Salle de visioconférence (Jitsi), notes de consultation
├── prescriptions/    # Ordonnances numériques
├── records/          # Dossier médical, documents, historique
├── notifications/    # Commande d'envoi des rappels automatiques
├── templates/         # Templates HTML (Bootstrap 5)
├── static/            # CSS / JS
└── visiocare/          # Configuration du projet (settings, urls, wsgi)
```

## Notes de sécurité pour une mise en production réelle

Ce projet est une base fonctionnelle à but pédagogique/démonstratif. Avant un
usage réel avec de vraies données de santé, prévoyez notamment :
chiffrement renforcé des données médicales, conformité RGPD/réglementation
locale sur les données de santé, journalisation des accès, authentification
à deux facteurs, hébergement conforme (HDS en France par exemple), et un
audit de sécurité complet.
