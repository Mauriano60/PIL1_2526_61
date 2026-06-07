'use strict';

/*INITIALISATION GLOBALE */

document.addEventListener('DOMContentLoaded', function () {

  /* Initialise tous les composants partagés */
  initialiserNavigation();
  initialiserModals();
  initialiserRecherche();

  console.info('[MentorLink] Application initialisée.');
});

/* NAVIGATION — Marque le lien actif selon l'URL */

/**
 * Détecte la page courante et applique la classe "actif"
 * au lien de navigation correspondant dans la sidebar.
 */
function initialiserNavigation() {

  /* Récupère le nom du fichier courant depuis l'URL */
  const urlCourante = window.location.pathname;
  const nomPage = urlCourante.split('/').pop() || 'index.html';

  /* Sélectionne tous les liens de la sidebar */
  const liens = document.querySelectorAll('.nav-lien[data-page]');

  liens.forEach(function (lien) {
    /* Retire la classe actif de tous */
    lien.classList.remove('actif');

    /* Applique la classe actif au lien correspondant à la page */
    if (lien.dataset.page === nomPage) {
      lien.classList.add('actif');
    }
  });
}

/* MODALS — Système de gestion des modals */

/**
 * Initialise l'écoute des clics sur les boutons qui ouvrent
 * ou ferment des modals. Utilise des attributs data-* pour
 * éviter le couplage entre HTML et JS.
 */
function initialiserModals() {

  /* Ouvre une modal au clic sur un déclencheur */
  document.querySelectorAll('[data-ouvrir-modal]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const idModal = btn.dataset.ouvrirModal;
      ouvrirModal(idModal);
    });
  });

  /* Ferme une modal au clic sur un bouton de fermeture */
  document.querySelectorAll('[data-fermer-modal]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const idModal = btn.dataset.fermerModal;
      fermerModal(idModal);
    });
  });

  /* Ferme une modal en cliquant sur l'overlay (fond sombre) */
  document.querySelectorAll('.modal-overlay').forEach(function (overlay) {
    overlay.addEventListener('click', function (e) {
      /* Vérifie qu'on clique bien sur l'overlay et pas sur la boîte */
      if (e.target === overlay) {
        overlay.classList.remove('visible');
      }
    });
  });

  /* Ferme une modal avec la touche Échap */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-overlay.visible').forEach(function (overlay) {
        overlay.classList.remove('visible');
      });
    }
  });
}

/**
 * Ouvre une modal par son ID.
 * @param {string} id - L'id de l'élément .modal-overlay
 */
function ouvrirModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.add('visible');
    /* Empêche le scroll du body pendant que la modal est ouverte */
    document.body.style.overflow = 'hidden';
  }
}

/**
 * Ferme une modal par son ID.
 * @param {string} id - L'id de l'élément .modal-overlay
 */
function fermerModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.remove('visible');
    document.body.style.overflow = '';
  }
}

/* Expose les fonctions globalement pour les onclick inline */
window.ouvrirModal = ouvrirModal;
window.fermerModal = fermerModal;

/* RECHERCHE GLOBALE (topbar) */

/**
 * Initialise la barre de recherche globale de la topbar.
 * Dans une vraie app, enverrait une requête à l'API Django.
 */
function initialiserRecherche() {
  const input = document.getElementById('rechercheGlobale');
  if (!input) return;

  input.addEventListener('input', debounce(function () {
    const texte = input.value.trim();
    if (texte.length < 2) return;
    /* TODO : appel API Django — GET /api/recherche/?q=texte */
    console.info('[Recherche] Requête :', texte);
  }, 300));
}

/* UTILITAIRES JAVASCRIPT */

/**
 * Retarde l'exécution d'une fonction jusqu'à ce que
 * l'utilisateur arrête de déclencher l'événement.
 *
 * @param {Function} fn - Fonction à exécuter
 * @param {number} delai - Délai en millisecondes
 * @returns {Function}
 */
function debounce(fn, delai) {
  let minuterie;
  return function (...args) {
    clearTimeout(minuterie);
    minuterie = setTimeout(function () { fn.apply(this, args); }, delai);
  };
}

/**
 * Met en majuscule la première lettre d'une chaîne.
 * @param {string} str
 * @returns {string}
 */
function capitaliser(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Formate une date ISO en date lisible française.
 * @param {string} iso - Date ISO 8601
 * @returns {string} Ex : "7 juin 2026"
 */
function formaterDate(iso) {
  return new Date(iso).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });
}

/**
 * Formate une heure ISO en heure locale.
 * @param {string} iso
 * @returns {string} Ex : "14:30"
 */
function formaterHeure(iso) {
  return new Date(iso).toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Tronque un texte à une longueur maximale.
 * @param {string} texte
 * @param {number} max
 * @returns {string}
 */
function tronquer(texte, max) {
  if (!texte || texte.length <= max) return texte;
  return texte.slice(0, max).trim() + '…';
}

/**
 * Génère un ID unique simple (pour les besoins frontend).
 * @returns {string}
 */
function genererID() {
  return Math.random().toString(36).slice(2, 9);
}

/**
 * Affiche un toast de notification temporaire.
 * @param {string} message - Texte du toast
 * @param {'succes'|'erreur'|'info'} type - Type de toast
 * @param {number} duree - Durée en ms (défaut 3500)
 */
function afficherToast(message, type = 'succes', duree = 3500) {

  /* Crée le conteneur de toasts s'il n'existe pas */
  let conteneur = document.getElementById('toast-conteneur');
  if (!conteneur) {
    conteneur = document.createElement('div');
    conteneur.id = 'toast-conteneur';
    conteneur.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 8px;
    `;
    document.body.appendChild(conteneur);
  }

  /* Couleurs selon le type */
  const couleurs = {
    succes: '#10b981',
    erreur: '#ef4444',
    info:   '#2563eb'
  };

  /* Crée l'élément toast */
  const toast = document.createElement('div');
  toast.style.cssText = `
    background: #0f172a;
    color: #ffffff;
    padding: 12px 18px;
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.875rem;
    font-weight: 500;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    border-left: 3px solid ${couleurs[type] || couleurs.info};
    max-width: 320px;
    opacity: 0;
    transform: translateX(12px);
    transition: opacity 0.2s ease, transform 0.2s ease;
  `;
  toast.textContent = message;
  conteneur.appendChild(toast);

  /* Animation d'entrée */
  requestAnimationFrame(function () {
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(0)';
  });

  /* Supprime le toast après la durée */
  setTimeout(function () {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(12px)';
    setTimeout(function () { toast.remove(); }, 200);
  }, duree);
}

/* Expose les utilitaires globalement */
window.debounce     = debounce;
window.capitaliser  = capitaliser;
window.formaterDate = formaterDate;
window.formaterHeure = formaterHeure;
window.tronquer     = tronquer;
window.genererID    = genererID;
window.afficherToast = afficherToast;