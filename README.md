# IFRI_MentorLink

Plateforme de mise en relation entre étudiants pour le mentorat académique.
Projet réalisé par des étudiants de L1 en 10 jours.

## Fonctionnalités

- **Inscription multi-étapes** : email, profil, compétences/lacunes (max 4), disponibilités
- **Catalogues** : offres et demandes de mentorat avec pagination (12/page)
- **Matching algorithmique** : score de compatibilité basé sur les annonces (40 %), disponibilités (30 %), filière (20 %), niveau (10 %)
- **Matching temps réel** : suggestions instantanées après publication d'une annonce
- **Notifications temps réel** : cloche mise à jour via SocketIO, avec boutons Accepter/Refuser
- **Messagerie temps réel** : conversations avec messages instantanés sans rechargement
- **Dashboard** : statistiques, dernières correspondances, publications actives
- **Paramètres** : profil, matières, disponibilités, confidentialité, suppression de compte
- **Sécurité** : CSRF, rate limiting, bcrypt, validation backend

## Technologies

### Backend
| Technologie | Utilisation |
|---|---|
| Python 3.13 | Langage serveur |
| Flask | Framework web (Blueprints) |
| Flask-SocketIO | Temps réel (WebSocket + fallback polling) |
| PyMySQL | Connecteur MySQL |
| Flask-Mail | Envoi d'emails |
| Flask-Limiter | Rate limiting (5 req/min sur login) |
| bcrypt | Hash des mots de passe |
| python-dotenv | Variables d'environnement |
| pytest | Tests unitaires |

### Base de données
- **MySQL 8.0**
- 15 tables : utilisateurs, matières, filières, niveaux, offres, demandes, correspondances, disponibilités, notifications, conversations, messages, participants, compétences, difficultés, préférences

### Frontend
- **HTML5 / Jinja2** — rendu serveur
- **Bootstrap 5.3** + **Bootstrap Icons**
- **CSS personnalisé** — thème bleu `#2563EB`
- **JavaScript vanilla** — SocketIO client, formulaires dynamiques
- **Google Fonts** — Inter + Poppins

## Prérequis

- Python 3.13+
- MySQL 8.0
- pip

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd PIL1_2526_61
```

### 2. Base de données

```bash
mysql -u root -p < backend/database/ifri_mentorlink.sql
```

### 3. Fichier `.env`

Crée ou modifie `backend/.env` :

```env
DB_NAME=ifri_mentorlink
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_USER=root
SECRET_KEY=une_cle_secrete
DEBUG=True
MAIL_USERNAME=votre_email@gmail.com
MAIL_PASSWORD=votre_mot_de_passe_app
```

> Le mode local (`MAIL_SUPPRESS_SEND = True`) affiche les emails dans la console au lieu de les envoyer.

### 4. Dépendances Python

```bash
cd backend
pip install -r requirements.txt
```

### 5. Lancer le serveur

```bash
python app.py
```

Le site est accessible sur **http://127.0.0.1:5000**

### 6. (Optionnel) Installer le transport WebSocket

```bash
pip install websocket-client
```

Sans ce package, SocketIO utilise le fallback HTTP long-polling (même comportement fonctionnel).

## Comptes de test

Mot de passe commun : `Test1234`

| Email | Rôle |
|---|---|
| `test.mamadou@test.com` | Mentor Python / Java |
| `test.fatou@test.com` | Mentee (cherche Python) |
| `test.awa@test.com` | Mentor Maths |
| `test.ibrahima@test.com` | Mentor IoT |
| `test.marie@test.com` | Mentee (cherche POO) |
| `test.yacouba@test.com` | Mentee (débutant Python) |
| `test.fanta@test.com` | Mentor Data Science |
| `test.ousmane@test.com` | Mentor Sécurité |
| `test.kadi@test.com` | Mentee (Web) |
| `test.moussa@test.com` | Mentor IoT |
| `test.aminata@test.com` | Mentor Web full-stack |
| `test.cheikh@test.com` | Mentee (Python, Maths) |

## Architecture

```
PIL1_2526_61/
├── backend/
│   ├── app.py                      # Point d'entrée + SocketIO events
│   ├── requirements.txt            # Dépendances Python
│   ├── config/settings.py          # Configuration (.env)
│   ├── db/database.py              # Connexion MySQL (fetch_one, fetch_all, execute)
│   ├── routes/
│   │   ├── auth.py                 # Inscription, connexion, déconnexion
│   │   ├── users.py                # Dashboard, profil public
│   │   ├── offres.py               # Offres de mentorat (catalogue + création)
│   │   ├── demandes.py             # Demandes d'aide (catalogue + création)
│   │   ├── matching.py             # Page matching + acceptation/refus
│   │   ├── notifications.py        # Notifications + acceptation/refus
│   │   ├── conversations.py        # Messagerie privée
│   │   ├── parametres.py           # Profil, matières, disponibilités
│   │   ├── email.py                # Vérification email, mot de passe oublié
│   │   └── references.py           # Données de référence
│   ├── services/
│   │   ├── matching_service.py     # Algorithme de scoring
│   │   ├── notification_service.py # Création + émission SocketIO
│   │   └── mail_service.py         # Envoi d'emails
│   ├── templates/                  # Jinja2
│   │   ├── auth/                   # Login, register (4 étapes)
│   │   ├── dashboard/              # Tableau de bord
│   │   ├── mentorat/               # Offres, demandes, création
│   │   ├── matching/               # Matching
│   │   ├── notifications/          # Notifications
│   │   ├── conversations/          # Messagerie
│   │   ├── settings/               # Paramètres (4 onglets)
│   │   └── profil/                 # Profil public
│   ├── static/
│   │   ├── css/                    # style.css, Bootstrap
│   │   ├── js/                     # socketio-client.js, Bootstrap
│   │   └── uploads/                # Avatars
│   ├── utils/
│   │   ├── responses.py            # Contexte utilisateur partagé
│   │   ├── validators.py           # Validation email, téléphone, mot de passe
│   │   └── csrf.py                 # Token CSRF + décorateur
│   └── database/
│       └── ifri_mentorlink.sql     # Schéma + données initiales
```

## Parcours complet

1. **Inscription** → `/register` (3 étapes : informations personnelles, profil académique, disponibilités)
2. **Dashboard** → vue d'ensemble des stats, matchs, publications
3. **Paramètres > Profil** → modifier ses compétences/lacunes/disponibilités
4. **Publier** → `/offres/creer` ou `/demandes/creer` → matching instantané automatique avec suggestions
5. **Explorer le catalogue** → `/offres` ou `/demandes` → cliquer "Calculer" sur une annonce pour voir la compatibilité
6. **Faire le match** → confirmer → notification envoyée à l'autre étudiant
7. **Accepter/Refuser** → depuis `/notifications` ou la cloche
8. **Discuter** → `/conversations` → messages temps réel

## Temps réel

- **SocketIO** (WebSocket + fallback polling)
- Client injecté automatiquement dans toutes les pages HTML par `@app.after_request`
- Événements : `nouvelle_notification` (cloche), `new_message` (messagerie), `send_message`, `join_conversation`

## Matching

### Matching automatique (après publication)
Quand un utilisateur publie une offre ou une demande, le système calcule automatiquement les compatibilités avec les annonces actives des autres étudiants et affiche jusqu'à 5 suggestions directement sur la page de confirmation.

### Matching manuel (via le catalogue)
Depuis `/offres` ou `/demandes`, l'utilisateur peut :
1. Cliquer **"Calculer"** sur une annonce pour voir le score de compatibilité, les matières et les créneaux communs
2. Cliquer **"Faire le match"** pour envoyer une demande
3. Le destinataire reçoit une notification avec **Accepter / Refuser**

### Algorithme de score

| Critère | Poids | Calcul |
|---|---|---|
| Annonces communes | 40 % | Offre de l'un ∩ Demande de l'autre |
| Disponibilités | 30 % | Chevauchement des créneaux horaires |
| Filière | 20 % | Même filière = 20 |
| Niveau | 10 % | Écart de niveau (3.0 si >= 3) |

Seuil minimum : **50/100** pour apparaître dans les suggestions.

## Tests

```bash
cd backend
pytest tests/ -v
```

## Scripts utilitaires

Des scripts de test sont disponibles dans `C:\Users\HP\AppData\Local\Temp\opencode\` :

- `creer_12_users.py` — crée 12 utilisateurs fictifs
- `supprimer_12_users.py` — supprime les utilisateurs fictifs
- `test_messages_realtime.py` — teste la messagerie temps réel
- `test_match_demande.py` — teste le flux matching + notification
- `test_refus.py` — teste le refus de match

## Auteurs

Projet réalisé par des étudiants de l'IFRI — L1, 7 jours.
