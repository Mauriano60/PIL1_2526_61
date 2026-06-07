'use strict';

/* DONNÉES DE NAVIGATION
   Centralise les liens de la sidebar en un seul endroit.
   Pour ajouter/modifier un lien, modifier uniquement ce tableau.*/

const LIENS_NAVIGATION = [
  {
    section: null, /* Pas de label de section pour le bloc principal */
    liens: [
      { page: 'dashboard.html', label: 'Dashboard',      badge: null },
      { page: 'profil.html',    label: 'Profil',         badge: null },
      { page: 'offres.html',    label: 'Offres',         badge: null },
      { page: 'demandes.html',  label: 'Demandes',       badge: null },
    ]
  },
  {
    section: 'Activité',
    liens: [
      { page: 'matching.html',      label: 'Matching',      badge: { texte: '12', classe: 'nav-badge--vert' } },
      { page: 'messages.html',      label: 'Messages',      badge: { texte: '5',  classe: 'nav-badge--rouge' } },
      { page: 'notifications.html', label: 'Notifications', badge: { texte: '3',  classe: 'nav-badge--orange' } },
    ]
  },
  {
    section: 'Système',
    liens: [
      { page: 'parametres.html', label: 'Paramètres', badge: null },
    ]
  }
];

/* DONNÉES UTILISATEUR (simulées — viendra de Django) */

const UTILISATEUR_COURANT = {
  initiales: 'U',
  nom: 'Utilisateur',
  filiere: 'Génie Logiciel',
  niveau: 'L1',
  couleurAvatar: 'bleu'
};

/* GÉNÉRATION HTML DE LA SIDEBAR*/

/**
 * Génère et injecte la sidebar dans l'élément
 * portant l'attribut data-composant="sidebar".
 * Appelé automatiquement au chargement du DOM.
 */
function monterSidebar() {
  const conteneur = document.querySelector('[data-composant="sidebar"]');
  if (!conteneur) return;

  conteneur.innerHTML = construireSidebarHTML();
  /* Marque le lien actif après injection */
  marquerLienActif();
}

/**
 * Construit le HTML complet de la sidebar.
 * @returns {string} HTML de la sidebar
 */
function construireSidebarHTML() {

  /*Logo */
  const htmlLogo = `
    <div class="sidebar-logo">
      <div class="logo-marque">
        <span class="logo-lettre">M</span>
      </div>
      <div class="logo-texte">
        <span class="logo-nom">MentorLink</span>
        <span class="logo-sous-titre">IFRI — UAC</span>
      </div>
    </div>
  `;

  /*Navigation */
  let htmlNav = '<nav class="sidebar-nav">';

  LIENS_NAVIGATION.forEach(function (groupe) {
    /* Label de section (si défini) */
    if (groupe.section) {
      htmlNav += `<div class="nav-section-label">${groupe.section}</div>`;
    }

    /* Liens du groupe */
    groupe.liens.forEach(function (lien) {
      /* Badge numérique (si défini) */
      const htmlBadge = lien.badge
        ? `<span class="nav-badge ${lien.badge.classe}">${lien.badge.texte}</span>`
        : '';

      htmlNav += `
        <a href="${lien.page}" class="nav-lien" data-page="${lien.page}">
          <span class="nav-lien-texte">${lien.label}</span>
          ${htmlBadge}
        </a>
      `;
    });
  });

  htmlNav += '</nav>';

  /* Séparateur + Déconnexion */
  const htmlDeconnexion = `
    <hr class="sidebar-separateur" />
    <a href="#" class="nav-lien nav-lien--deconnexion" onclick="deconnecter(event)">
      <span class="nav-lien-texte">Déconnexion</span>
    </a>
  `;

  /* ---- Profil utilisateur en bas ---- */
  const htmlUtilisateur = `
    <div class="sidebar-utilisateur">
      <div class="avatar avatar--sm avatar--${UTILISATEUR_COURANT.couleurAvatar}">
        ${UTILISATEUR_COURANT.initiales}
      </div>
      <div class="sidebar-utilisateur-info">
        <div class="sidebar-utilisateur-nom">${UTILISATEUR_COURANT.nom}</div>
        <div class="sidebar-utilisateur-role">
          ${UTILISATEUR_COURANT.filiere} · ${UTILISATEUR_COURANT.niveau}
        </div>
      </div>
    </div>
  `;

  return htmlLogo + htmlNav + htmlDeconnexion + htmlUtilisateur;
}

/**
 * Marque le lien de navigation correspondant à la page courante.
 */
function marquerLienActif() {
  const nomPage = window.location.pathname.split('/').pop() || 'dashboard.html';
  const liens = document.querySelectorAll('.nav-lien[data-page]');

  liens.forEach(function (lien) {
    lien.classList.remove('actif');
    if (lien.dataset.page === nomPage) {
      lien.classList.add('actif');
    }
  });
}

/**
 * Simule la déconnexion (dans une vraie app : POST /api/auth/deconnexion/).
 * @param {Event} e
 */
function deconnecter(e) {
  e.preventDefault();
  if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
    /* TODO : appel API Django — POST /api/auth/deconnecter/ */
    window.location.href = 'connexion.html';
  }
}

window.deconnecter = deconnecter;

/* Lance le montage au chargement du DOM */
document.addEventListener('DOMContentLoaded', monterSidebar);