'use strict';

/* DONNÉES — Préférences de notifications */

const TOGGLES_NOTIFICATIONS = [
  {
    id: 'notif-matching',
    label: 'Nouvelles correspondances',
    description: 'Recevoir une notification lorsqu\'un mentor compatible est trouvé.',
    active: true,
  },
  {
    id: 'notif-messages',
    label: 'Nouveaux messages',
    description: 'Être alerté à chaque message reçu dans la messagerie.',
    active: true,
  },
  {
    id: 'notif-demandes',
    label: 'Demandes de mentorat',
    description: 'Recevoir une notification lorsqu\'une demande vous est envoyée.',
    active: true,
  },
  {
    id: 'notif-rappels',
    label: 'Rappels de séances',
    description: 'Rappels 30 minutes avant une session de mentorat planifiée.',
    active: false,
  },
  {
    id: 'notif-systeme',
    label: 'Notifications système',
    description: 'Mises à jour de la plateforme, maintenance, nouvelles fonctionnalités.',
    active: false,
  },
];

/* DONNÉES — Préférences de confidentialité */

const TOGGLES_CONFIDENTIALITE = [
  {
    id: 'conf-profil-public',
    label: 'Profil visible par tous',
    description: 'Votre profil peut être vu par tous les étudiants connectés.',
    active: true,
  },
  {
    id: 'conf-disponibilites',
    label: 'Afficher mes disponibilités',
    description: 'Les créneaux horaires sont visibles sur votre profil public.',
    active: true,
  },
  {
    id: 'conf-filiere',
    label: 'Afficher ma filière et mon niveau',
    description: 'Ces informations apparaissent dans les résultats de matching.',
    active: true,
  },
  {
    id: 'conf-messages-directs',
    label: 'Autoriser les messages directs',
    description: 'N\'importe quel étudiant peut vous envoyer un message sans match préalable.',
    active: false,
  },
];

/* INITIALISATION — DOMContentLoaded */

document.addEventListener('DOMContentLoaded', function () {
  /* Génère les toggles de notifications et de confidentialité */
  rendreLignesToggle('togglesNotifs',       TOGGLES_NOTIFICATIONS);
  rendreLignesToggle('togglesConf',         TOGGLES_CONFIDENTIALITE);
  /* Indicateur de force du mot de passe */
  initialiserForceMdp();
});

/* NAVIGATION ENTRE SECTIONS */

/**
 * Affiche la section de paramètres correspondante
 * et met à jour le bouton de navigation actif.
 * @param {string}      idSection - 'compte' | 'notifications' | 'confidentialite' | 'securite'
 * @param {HTMLElement} el        - Bouton cliqué
 */
function changerSection(idSection, el) {
  /* Masque toutes les sections */
  document.querySelectorAll('.param-section').forEach(function (s) {
    s.classList.add('cache');
  });

  /* Affiche la section cible */
  const cible = document.getElementById('section' + capitaliser(idSection));
  if (cible) {
    cible.classList.remove('cache');
  }

  /* Mise à jour du bouton actif */
  document.querySelectorAll('.param-nav-item').forEach(function (b) {
    b.classList.remove('actif');
  });
  if (el) {
    el.classList.add('actif');
  }
}

/**
 * Met en majuscule la première lettre d'une chaîne.
 * @param {string} str
 * @returns {string}
 */
function capitaliser(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/* GÉNÉRATION DES LIGNES TOGGLE */

/**
 * Génère et injecte des lignes de toggle switch dans un conteneur.
 * @param {string} idConteneur  - ID de l'élément cible
 * @param {Array}  donnees      - Tableau de configuration des toggles
 */
function rendreLignesToggle(idConteneur, donnees) {
  const conteneur = document.getElementById(idConteneur);
  if (!conteneur) return;

  conteneur.innerHTML = donnees.map(function (t) {
    return `
      <div class="toggle-ligne">
        <div class="toggle-info">
          <div class="toggle-label">${t.label}</div>
          <div class="toggle-description">${t.description}</div>
        </div>
        <label class="toggle-switch" aria-label="${t.label}">
          <input
            type="checkbox"
            id="${t.id}"
            ${t.active ? 'checked' : ''}
            onchange="changerToggle('${t.id}', this.checked)"
          />
          <span class="toggle-curseur"></span>
        </label>
      </div>
    `;
  }).join('');
}

/**
 * Réagit au changement d'état d'un toggle.
 * @param {string}  id     - Identifiant du toggle
 * @param {boolean} actif  - Nouvel état
 */
function changerToggle(id, actif) {
  /* Met à jour les données en mémoire */
  [TOGGLES_NOTIFICATIONS, TOGGLES_CONFIDENTIALITE].forEach(function (tableau) {
    const toggle = tableau.find(function (t) { return t.id === id; });
    if (toggle) {
      toggle.active = actif;
    }
  });
  /* TODO : envoyer PATCH /api/utilisateurs/moi/preferences/ avec {id, actif} */
  afficherToast(
    actif ? 'Préférence activée.' : 'Préférence désactivée.',
    'succes'
  );
}

/* SECTION COMPTE — Sauvegarde des informations */

/**
 * Valide et sauvegarde les informations du compte.
 * TODO : remplacer par PATCH /api/utilisateurs/moi/
 */
function sauvegarderCompte() {
  const prenom  = document.getElementById('pPrenom')?.value.trim();
  const nom     = document.getElementById('pNom')?.value.trim();
  const email   = document.getElementById('pEmail')?.value.trim();
  const filiere = document.getElementById('pFiliere')?.value;
  const niveau  = document.getElementById('pNiveau')?.value;

  if (!prenom || !email) {
    afficherToast('Le prénom et l\'e-mail sont obligatoires.', 'erreur');
    return;
  }

  if (!email.includes('@')) {
    afficherToast('L\'adresse e-mail n\'est pas valide.', 'erreur');
    return;
  }

  /* Simulation de sauvegarde réussie */
  afficherToast('Informations enregistrées avec succès.', 'succes');

  /* TODO : mettre à jour le nom dans la sidebar */
  console.log('[Paramètres] Compte à sauvegarder :', { prenom, nom, email, filiere, niveau });
}

/* SECTION SÉCURITÉ — Changement de mot de passe */

/**
 * Valide et soumet le changement de mot de passe.
 * TODO : remplacer par POST /api/auth/changer-mot-de-passe/
 */
function changerMotDePasse() {
  const actuel   = document.getElementById('mdpActuel')?.value;
  const nouveau  = document.getElementById('mdpNouveau')?.value;
  const confirm  = document.getElementById('mdpConfirm')?.value;

  if (!actuel || !nouveau || !confirm) {
    afficherToast('Veuillez remplir tous les champs de mot de passe.', 'erreur');
    return;
  }

  if (nouveau.length < 8) {
    afficherToast('Le nouveau mot de passe doit faire au moins 8 caractères.', 'erreur');
    return;
  }

  if (!/[A-Z]/.test(nouveau) || !/[0-9]/.test(nouveau)) {
    afficherToast('Le mot de passe doit contenir une majuscule et un chiffre.', 'erreur');
    return;
  }

  if (nouveau !== confirm) {
    afficherToast('Les deux mots de passe ne correspondent pas.', 'erreur');
    return;
  }

  /* Simulation — dans la vraie app : POST /api/auth/changer-mot-de-passe/ */
  afficherToast('Mot de passe modifié avec succès.', 'succes');

  /* Vide les champs après succès */
  ['mdpActuel', 'mdpNouveau', 'mdpConfirm'].forEach(function (id) {
    const el = document.getElementById(id);
    if (el) { el.value = ''; }
  });

  /* Réinitialise l'indicateur de force */
  mettreAJourForceMdp('');
}

/* INDICATEUR DE FORCE DU MOT DE PASSE */

/**
 * Attache l'écouteur d'événement sur le champ de nouveau mot de passe.
 */
function initialiserForceMdp() {
  /* Crée le bloc d'indicateur et l'injecte sous le champ */
  const champNouveau = document.getElementById('mdpNouveau');
  if (!champNouveau) return;

  const indicateur = document.createElement('div');
  indicateur.id = 'indicateurForceMdp';
  indicateur.className = 'force-mdp';
  indicateur.innerHTML = `
    <div class="force-mdp-barres">
      <div class="force-mdp-barre" id="barre1"></div>
      <div class="force-mdp-barre" id="barre2"></div>
      <div class="force-mdp-barre" id="barre3"></div>
    </div>
    <div class="force-mdp-texte" id="forceMdpTexte">Saisissez un mot de passe</div>
  `;

  /* Insère après le champ */
  champNouveau.parentNode.insertBefore(indicateur, champNouveau.nextSibling);

  /* Écoute les modifications */
  champNouveau.addEventListener('input', function () {
    mettreAJourForceMdp(this.value);
  });
}

/**
 * Calcule et affiche la force du mot de passe.
 * @param {string} mdp
 */
function mettreAJourForceMdp(mdp) {
  const b1    = document.getElementById('barre1');
  const b2    = document.getElementById('barre2');
  const texte = document.getElementById('forceMdpTexte');
  const b3    = document.getElementById('barre3');

  if (!b1 || !b2 || !b3 || !texte) return;

  /* Réinitialise les barres */
  [b1, b2, b3].forEach(function (b) {
    b.className = 'force-mdp-barre';
  });
  texte.className = 'force-mdp-texte';

  if (!mdp) {
    texte.textContent = 'Saisissez un mot de passe';
    return;
  }

  /* Calcul du score */
  let score = 0;
  if (mdp.length >= 8)           { score++; }
  if (/[A-Z]/.test(mdp))         { score++; }
  if (/[0-9]/.test(mdp))         { score++; }
  if (/[^A-Za-z0-9]/.test(mdp))  { score++; }
  if (mdp.length >= 12)          { score++; }

  /* Affichage selon le niveau */
  if (score <= 2) {
    b1.classList.add('active--faible');
    texte.textContent = 'Faible';
    texte.classList.add('faible');
  } else if (score <= 3) {
    b1.classList.add('active--moyen');
    b2.classList.add('active--moyen');
    texte.textContent = 'Moyen';
    texte.classList.add('moyen');
  } else {
    b1.classList.add('active--fort');
    b2.classList.add('active--fort');
    b3.classList.add('active--fort');
    texte.textContent = 'Fort';
    texte.classList.add('fort');
  }
}

/*SUPPRESSION DU COMPTE*/

/**
 * Ouvre une modal de confirmation avant de supprimer le compte.
 * TODO : brancher sur la modal de composants.css une fois disponible.
 */
function confirmerSuppression() {
  const confirme = window.confirm(
    'Êtes-vous sûr de vouloir supprimer votre compte ?\n' +
    'Cette action est irréversible. Toutes vos données seront supprimées.'
  );

  if (confirme) {
    /* TODO : DELETE /api/utilisateurs/moi/ */
    afficherToast('Compte supprimé. Redirection…', 'succes');
    setTimeout(function () {
      window.location.href = 'connexion.html';
    }, 1500);
  }
}

/* EXPOSITION GLOBALE
   Fonctions appelées depuis les attributs onclick du HTML. */

window.changerSection      = changerSection;
window.changerToggle       = changerToggle;
window.sauvegarderCompte   = sauvegarderCompte;
window.changerMotDePasse   = changerMotDePasse;
window.confirmerSuppression = confirmerSuppression;