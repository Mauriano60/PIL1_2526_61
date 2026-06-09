/* ============================================================
   script3.js — Logique JavaScript de l'étape 3 : Disponibilités
   Fonctionnalités :
     - Affichage/masquage du formulaire de créneau
     - Validation des champs du formulaire
     - Ajout et suppression de créneaux
     - Validation finale et simulation de création de compte
     - Affichage de notifications temporaires
   ============================================================ */

/* ============================================================
   ÉTAT GLOBAL DE L'APPLICATION
   ============================================================ */

/* Tableau qui stocke tous les créneaux confirmés par l'utilisateur */
/* Chaque élément est un objet : { id, jour, debut, fin } */
let creneaux = [];

/* Compteur d'identifiant unique pour chaque créneau */
/* Incrémenté à chaque ajout pour éviter les doublons d'ID */
let compteurId = 0;

/* ============================================================
   INITIALISATION AU CHARGEMENT DE LA PAGE
   ============================================================ */

/* Attend que tout le DOM soit chargé avant d'exécuter le code */
document.addEventListener('DOMContentLoaded', function () {

  /* Affiche un message de confirmation dans la console du navigateur */
  console.log('IFRI_ MentorLink — Étape 3 : Disponibilités chargée.');

  /* Affiche la liste vide au départ (ne rien afficher) */
  afficherCreneaux();
  /* Appelle la fonction d'affichage dès le départ pour initialiser l'état */
});

/* ============================================================
   GESTION DU FORMULAIRE INLINE DE CRÉNEAU
   ============================================================ */

/**
 * Affiche le formulaire inline d'ajout de créneau.
 * Appelée au clic sur le bouton "Ajouter un créneau".
 */
function ouvrirFormCreneau() {

  /* Récupère l'élément du formulaire par son ID */
  const form = document.getElementById('formCreneau');

  /* Rend le formulaire visible en retirant la classe Bootstrap d-none */
  form.classList.remove('d-none');
  /* d-none = display:none en CSS Bootstrap → le retirer affiche l'élément */

  /* Cache le bouton "Ajouter un créneau" pour éviter deux formulaires ouverts */
  const btnAjouter = document.getElementById('btnAjouter');
  btnAjouter.classList.add('d-none');
  /* On le cachera jusqu'à confirmation ou annulation */

  /* Remet tous les champs du formulaire à zéro */
  document.getElementById('creneauJour').value  = '';  /* Vide le select Jour */
  document.getElementById('creneauDebut').value = '';  /* Vide l'heure de début */
  document.getElementById('creneauFin').value   = '';  /* Vide l'heure de fin */

  /* Retire les éventuels états d'erreur précédents des champs */
  ['creneauJour', 'creneauDebut', 'creneauFin'].forEach(function (id) {
    document.getElementById(id).classList.remove('is-invalid');
    /* is-invalid : classe Bootstrap qui ajoute une bordure rouge */
  });

  /* Place le focus sur le select Jour pour faciliter la saisie au clavier */
  document.getElementById('creneauJour').focus();
  /* focus() : active le champ sans que l'utilisateur clique dessus */
}

/**
 * Cache le formulaire inline sans sauvegarder les données saisies.
 * Appelée au clic sur le bouton Annuler (icône ✕).
 */
function annulerFormCreneau() {

  /* Cache le formulaire en ajoutant la classe d-none */
  document.getElementById('formCreneau').classList.add('d-none');

  /* Réaffiche le bouton "Ajouter un créneau" */
  document.getElementById('btnAjouter').classList.remove('d-none');
}

/* ============================================================
   VALIDATION ET AJOUT D'UN CRÉNEAU
   ============================================================ */

/**
 * Valide les champs du formulaire et ajoute le créneau à la liste.
 * Appelée au clic sur le bouton Confirmer (icône ✓ verte).
 */
function confirmerCreneau() {

  /* ---- Récupération des valeurs des trois champs ---- */

  /* Valeur du select Jour (ex: "Lundi", "" si rien sélectionné) */
  const jour  = document.getElementById('creneauJour').value;

  /* Valeur de l'heure de début (ex: "17:00", "" si vide) */
  const debut = document.getElementById('creneauDebut').value;

  /* Valeur de l'heure de fin (ex: "21:00", "" si vide) */
  const fin   = document.getElementById('creneauFin').value;

  /* ---- Réinitialisation des états d'erreur précédents ---- */
  ['creneauJour', 'creneauDebut', 'creneauFin'].forEach(function (id) {
    document.getElementById(id).classList.remove('is-invalid');
    /* Retire la bordure rouge Bootstrap de chaque champ */
  });

  /* ---- Indicateur global de validité du formulaire ---- */
  let formulaireValide = true;
  /* On suppose que tout est correct, puis on invalide si besoin */

  /* ---- Validation du champ Jour ---- */
  if (!jour) {
    /* Le champ Jour est vide (aucune option sélectionnée) */
    document.getElementById('creneauJour').classList.add('is-invalid');
    /* is-invalid : ajoute une bordure rouge et affiche le message d'erreur */
    formulaireValide = false; /* Le formulaire n'est plus valide */
  }

  /* ---- Validation du champ Heure de début ---- */
  if (!debut) {
    /* Le champ heure de début est vide */
    document.getElementById('creneauDebut').classList.add('is-invalid');
    formulaireValide = false;
  }

  /* ---- Validation du champ Heure de fin ---- */
  if (!fin) {
    /* Le champ heure de fin est vide */
    document.getElementById('creneauFin').classList.add('is-invalid');
    formulaireValide = false;
  }

  /* ---- Validation logique : la fin doit être après le début ---- */
  if (debut && fin && fin <= debut) {
    /* Les deux champs sont remplis mais la fin est avant ou égale au début */
    document.getElementById('creneauFin').classList.add('is-invalid');
    /* Signale l'erreur sur le champ de fin */
    afficherNotification('L\'heure de fin doit être après l\'heure de début.', 'danger');
    /* Affiche un message d'erreur explicatif */
    formulaireValide = false;
  }

  /* ---- Vérification des doublons (même jour déjà ajouté) ---- */
  if (formulaireValide) {
    /* On ne vérifie les doublons que si les champs de base sont valides */

    const jourDejaAjoute = creneaux.some(function (creneau) {
      return creneau.jour === jour;
      /* some() : retourne true si au moins un créneau a le même jour */
    });

    if (jourDejaAjoute) {
      /* Un créneau pour ce jour de la semaine existe déjà */
      document.getElementById('creneauJour').classList.add('is-invalid');
      afficherNotification(`Un créneau pour le ${jour} est déjà ajouté.`, 'danger');
      formulaireValide = false;
    }
  }

  /* ---- Si tout est valide : créer et ajouter le créneau ---- */
  if (formulaireValide) {

    /* Incrémente le compteur pour obtenir un ID unique */
    compteurId++;
    /* compteurId passe de 0 → 1 au premier ajout, 1 → 2 au second, etc. */

    /* Crée l'objet représentant le nouveau créneau */
    const nouveauCreneau = {
      id: compteurId,  /* Identifiant unique pour pouvoir supprimer ce créneau */
      jour: jour,      /* Jour de la semaine (ex: "Lundi") */
      debut: debut,    /* Heure de début (ex: "17:00") */
      fin: fin         /* Heure de fin (ex: "21:00") */
    };

    /* Ajoute l'objet à la fin du tableau global des créneaux */
    creneaux.push(nouveauCreneau);
    /* push() : ajoute l'élément comme dernier élément du tableau */

    /* Rafraîchit l'affichage de tous les créneaux dans la liste HTML */
    afficherCreneaux();

    /* Ferme le formulaire et réaffiche le bouton "Ajouter un créneau" */
    annulerFormCreneau();

    /* Affiche un log dans la console pour le débogage */
    console.log('Créneau ajouté :', nouveauCreneau);
    console.log('Tous les créneaux :', creneaux);
  }
  /* Si formulaireValide est false, les erreurs sont déjà affichées */
}

/* ============================================================
   SUPPRESSION D'UN CRÉNEAU
   ============================================================ */

/**
 * Supprime un créneau de la liste par son identifiant unique.
 * Appelée au clic sur le bouton ✕ d'un tag de créneau.
 *
 * @param {number} id - L'identifiant unique du créneau à supprimer
 */
function supprimerCreneau(id) {

  /* Filtre le tableau pour ne garder que les créneaux dont l'ID est différent */
  creneaux = creneaux.filter(function (creneau) {
    return creneau.id !== id;
    /* filter() retourne un nouveau tableau sans l'élément dont id === id paramètre */
  });

  /* Rafraîchit l'affichage après suppression */
  afficherCreneaux();

  /* Log de débogage dans la console */
  console.log(`Créneau supprimé (id: ${id}). Créneaux restants :`, creneaux);
}

/* ============================================================
   AFFICHAGE DE LA LISTE DES CRÉNEAUX
   ============================================================ */

/**
 * Génère le HTML de tous les créneaux et l'injecte dans le DOM.
 * Appelée après chaque ajout ou suppression de créneau.
 */
function afficherCreneaux() {

  /* Récupère le conteneur HTML de la liste des créneaux */
  const liste = document.getElementById('listeCréneaux');

  /* Vide complètement le conteneur avant de le reconstruire */
  liste.innerHTML = '';
  /* innerHTML = '' : supprime tout le HTML enfant du conteneur */

  /* Si le tableau est vide, on ne génère rien et on sort */
  if (creneaux.length === 0) {
    return; /* Sort de la fonction immédiatement */
  }

  /* Boucle sur chaque créneau pour construire et injecter son tag HTML */
  creneaux.forEach(function (creneau) {

    /* Construit la chaîne HTML du tag de créneau */
    const tagHTML = `

      <div class="creneau-tag" id="tag-${creneau.id}">
        <!-- id unique pour référencer ce tag dans le DOM si besoin -->

        <!-- Zone gauche : icône horloge + informations textuelles -->
        <div class="creneau-info">

          <!-- Icône horloge Bootstrap Icons -->
          <i class="bi bi-clock creneau-icon"></i>

          <!-- Texte : Jour en gras + plage horaire -->
          <div>

            <!-- Nom du jour (ex: Lundi) -->
            <span class="creneau-jour">${creneau.jour}</span>

            <!-- Plage horaire (ex: 17:00 - 21:00) avec marge gauche -->
            <span class="creneau-heures ms-2">${creneau.debut} – ${creneau.fin}</span>
            <!-- ms-2 : marge gauche Bootstrap de 0.5rem -->
            <!-- – : tiret demi-cadratin (plus joli que le tiret court) -->

          </div>
        </div>
        <!-- Fin zone gauche -->

        <!-- Bouton de suppression : icône ✕ à droite -->
        <button
          type="button"
          class="btn-supprimer-creneau"
          onclick="supprimerCreneau(${creneau.id})"
          title="Supprimer ce créneau"
        >
          <!-- onclick : appelle supprimerCreneau avec l'ID du créneau -->
          <!-- title : info-bulle au survol -->
          <i class="bi bi-x-lg"></i>
          <!-- bi-x-lg : icône croix de Bootstrap Icons -->
        </button>

      </div>
      <!-- Fin creneau-tag -->
    `;

    /* Injecte le HTML du tag à la fin du conteneur de liste */
    liste.insertAdjacentHTML('beforeend', tagHTML);
    /* insertAdjacentHTML('beforeend') : ajoute comme dernier enfant du conteneur */
  });
}

/* ============================================================
   VALIDATION FINALE ET CRÉATION DU COMPTE
   ============================================================ */

/**
 * Valide l'étape 3 et simule la création du compte utilisateur.
 * Appelée au clic sur le bouton "Créer mon compte ✓".
 */
function creerCompte() {

  /* ---- Vérification : au moins un créneau doit être ajouté ---- */
  if (creneaux.length === 0) {
    /* Aucun créneau n'a été ajouté → affiche une erreur */

    /* Affiche une notification d'erreur en rouge */
    afficherNotification(
      'Veuillez ajouter au moins un créneau de disponibilité avant de créer votre compte.',
      'danger'
    );

    /* Attire visuellement l'attention sur le bouton "Ajouter un créneau" */
    const btnAjouter = document.getElementById('btnAjouter');
    btnAjouter.style.borderColor = '#ef4444'; /* Passe la bordure en rouge */
    btnAjouter.style.color       = '#ef4444'; /* Passe le texte en rouge */

    /* Remet le bouton en bleu après 2 secondes */
    setTimeout(function () {
      btnAjouter.style.borderColor = '#2563eb'; /* Retour au bleu */
      btnAjouter.style.color       = '#2563eb'; /* Retour au bleu */
    }, 2000);
    /* setTimeout : exécute la fonction après 2000 millisecondes (2 secondes) */

    return; /* Arrête l'exécution de la fonction ici */
  }

  /* ---- Prépare l'objet des données de l'étape 3 ---- */
  const donneesEtape3 = {
    creneaux: creneaux
    /* Dans une vraie application, on ajouterait aussi les données des étapes 1 et 2 */
    /* récupérées depuis le localStorage ou un état global partagé */
  };

  /* Affiche les données collectées dans la console du navigateur */
  console.log('Étape 3 validée — Données :', donneesEtape3);
  console.log('Compte en cours de création...');

  /* ---- Affiche une notification de succès ---- */
  afficherNotification(
    'Compte créé avec succès ! Redirection vers votre tableau de bord...',
    'success'
  );

  /* ---- Simulation d'une redirection après 2 secondes ---- */
  setTimeout(function () {
    /* Dans une vraie application : */
    /* window.location.href = 'dashboard.html'; */
    console.log('Redirection vers le tableau de bord (simulation).');
  }, 2000);
}

/* ============================================================
   NAVIGATION : RETOUR À L'ÉTAPE 2
   ============================================================ */

/**
 * Redirige l'utilisateur vers la page de l'étape 2.
 * Appelée au clic sur le bouton "← Retour".
 */
function retourEtape2() {

  /* Dans une vraie application : */
  /* window.location.href = 'etape2.html'; */

  /* Pour la démo : affiche une notification informative */
  afficherNotification('Retour à l\'étape 2 : Profil académique.', 'info');

  /* Log dans la console */
  console.log('Navigation vers l\'étape 2 : Profil académique.');
}

/* ============================================================
   NOTIFICATION TEMPORAIRE BOOTSTRAP
   ============================================================ */

/**
 * Affiche une alerte Bootstrap colorée dans la zone dédiée.
 * La notification disparaît automatiquement après 4 secondes.
 *
 * @param {string} message - Le texte à afficher dans l'alerte
 * @param {string} type    - Type d'alerte Bootstrap :
 *                           'success' (vert), 'danger' (rouge), 'info' (bleu)
 */
function afficherNotification(message, type) {

  /* Récupère la zone d'alerte dédiée dans le HTML */
  const zone = document.getElementById('zoneAlerte');

  /* Vide la zone pour remplacer une éventuelle alerte précédente */
  zone.innerHTML = '';

  /* Construit et injecte le HTML de l'alerte Bootstrap */
  zone.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show mb-3" role="alert">
      <!-- alert-${type} : couleur de l'alerte selon le type -->
      <!-- alert-dismissible : permet la fermeture manuelle -->
      <!-- fade show : animation d'apparition Bootstrap -->
      <!-- role="alert" : accessibilité pour les lecteurs d'écran -->

      <span>${message}</span>
      <!-- Texte du message de notification -->

      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fermer"></button>
      <!-- data-bs-dismiss="alert" : Bootstrap ferme l'alerte au clic sans JS supplémentaire -->
    </div>
  `;

  /* Fait disparaître automatiquement l'alerte après 4 secondes */
  setTimeout(function () {
    zone.innerHTML = '';
    /* Vide la zone : supprime l'alerte du DOM après le délai */
  }, 4000);
  /* 4000 millisecondes = 4 secondes */
}
