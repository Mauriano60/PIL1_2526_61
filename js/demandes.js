'use strict';

/* DONNÉES SIMULÉES */

const DEMANDES_RECUES = [
  {
    id: 1,
    initiales: 'AM',
    couleur: 'violet',
    nom: 'Adjoa Mensah',
    filiere: 'IM · L1',
    matiere: 'Python',
    matiereClasse: 'badge-matiere--python',
    message: 'Bonjour, j\'aurais besoin d\'aide pour comprendre les bases de Python, notamment les fonctions et les listes. Pourriez-vous m\'accompagner ?',
    date: 'Il y a 2h',
    statut: 'attente'
  },
  {
    id: 2,
    initiales: 'BK',
    couleur: 'teal',
    nom: 'Bienvenu Kpodo',
    filiere: 'GL · L2',
    matiere: 'Algorithmique',
    matiereClasse: 'badge-matiere--algo',
    message: 'Je prépare mon examen de fin de semestre en algorithmique et j\'ai du mal avec les arbres binaires. Une session serait très utile.',
    date: 'Hier',
    statut: 'attente'
  },
];

const DEMANDES_ENVOYEES = [
  {
    id: 3,
    initiales: 'MH',
    couleur: 'bleu',
    nom: 'Marie Houngbédji',
    filiere: 'GL · M1',
    matiere: 'Python',
    matiereClasse: 'badge-matiere--python',
    message: 'Je souhaite approfondir mes connaissances en Pandas pour mon projet de data science.',
    date: 'Il y a 3 jours',
    statut: 'accepte'
  },
  {
    id: 4,
    initiales: 'PA',
    couleur: 'violet',
    nom: 'Paul Adéoti',
    filiere: 'GL · L3',
    matiere: 'SQL',
    matiereClasse: 'badge-matiere--sql',
    message: 'J\'aimerais que vous m\'aidiez à optimiser mes requêtes SQL pour mon projet de BDD.',
    date: 'Il y a 5 jours',
    statut: 'attente'
  },
  {
    id: 5,
    initiales: 'AK',
    couleur: 'teal',
    nom: 'Aminata Kora',
    filiere: 'SI · M2',
    matiere: 'Dev Web',
    matiereClasse: 'badge-matiere--devweb',
    message: 'Je travaille sur un projet React et j\'aurais besoin de conseils sur la gestion du state.',
    date: 'Il y a 1 semaine',
    statut: 'refuse'
  },
];

const DEMANDES_TERMINEES = [
  {
    id: 6,
    initiales: 'KM',
    couleur: 'indigo',
    nom: 'Kofi Mensah',
    filiere: 'GL · L2',
    matiere: 'Algorithmique',
    matiereClasse: 'badge-matiere--algo',
    message: 'Session sur les graphes et le parcours en largeur.',
    date: 'Il y a 2 semaines',
    statut: 'termine',
    note: 5
  },
];

/*INITIALISATION */

document.addEventListener('DOMContentLoaded', function () {
  rendreRecues();
  rendreEnvoyees();
  rendreTerminees();
});

/* ONGLETS */

/**
 * Change l'onglet actif et affiche le panneau correspondant.
 * @param {string} onglet - 'recues' | 'envoyees' | 'terminees'
 * @param {HTMLElement} el - L'élément bouton cliqué
 */
function changerOnglet(onglet, el) {
  /* Désactive tous les onglets */
  document.querySelectorAll('.onglet').forEach(function (btn) {
    btn.classList.remove('actif');
  });
  el.classList.add('actif');

  /* Cache tous les panneaux */
  ['panneauRecues', 'panneauEnvoyees', 'panneauTerminees'].forEach(function (id) {
    document.getElementById(id)?.classList.add('cache');
  });

  /* Affiche le panneau actif */
  const map = {
    recues:    'panneauRecues',
    envoyees:  'panneauEnvoyees',
    terminees: 'panneauTerminees',
  };
  document.getElementById(map[onglet])?.classList.remove('cache');
}

window.changerOnglet = changerOnglet;

/* RENDU DES LISTES */

function rendreRecues() {
  const conteneur = document.getElementById('listeRecues');
  if (!conteneur) return;

  if (DEMANDES_RECUES.length === 0) {
    conteneur.innerHTML = etatVide('Aucune demande reçue', 'Les demandes d\'autres étudiants apparaîtront ici.');
    return;
  }

  conteneur.innerHTML = DEMANDES_RECUES.map(function (d) {
    return carteDemandeRecue(d);
  }).join('');
}

function rendreEnvoyees() {
  const conteneur = document.getElementById('listeEnvoyees');
  if (!conteneur) return;

  if (DEMANDES_ENVOYEES.length === 0) {
    conteneur.innerHTML = etatVide('Aucune demande envoyée', 'Vos demandes de mentorat apparaîtront ici.');
    return;
  }

  conteneur.innerHTML = DEMANDES_ENVOYEES.map(function (d) {
    return carteDemandeEnvoyee(d);
  }).join('');
}

function rendreTerminees() {
  const conteneur = document.getElementById('listeTerminees');
  if (!conteneur) return;

  if (DEMANDES_TERMINEES.length === 0) {
    conteneur.innerHTML = etatVide('Aucune session terminée', 'Vos sessions passées apparaîtront ici.');
    return;
  }

  conteneur.innerHTML = DEMANDES_TERMINEES.map(function (d) {
    return carteDemandeTerminee(d);
  }).join('');
}

/* TEMPLATES HTML DES CARTES*/

function carteDemandeRecue(d) {
  return `
    <div class="demande-carte" data-id="${d.id}">
      <div class="demande-indicateur demande-indicateur--attente"></div>
      <div class="avatar avatar--md avatar--${d.couleur}">${d.initiales}</div>
      <div class="demande-corps">
        <div class="demande-entete">
          <div>
            <div class="demande-nom">${d.nom}</div>
            <div class="demande-meta">${d.filiere}</div>
          </div>
          <div class="flex items-centre gap-2">
            <span class="badge-matiere ${d.matiereClasse}">${d.matiere.toUpperCase()}</span>
            <span class="demande-date">${d.date}</span>
          </div>
        </div>
        <div class="demande-message">"${d.message}"</div>
        <div class="demande-actions">
          <button class="btn btn--primaire btn--sm" onclick="accepterDemande(${d.id})">Accepter</button>
          <button class="btn btn--secondaire btn--sm" onclick="refuserDemande(${d.id})">Refuser</button>
          <button class="btn btn--ghost btn--sm" onclick="voirProfil('${d.nom}')">Voir le profil</button>
        </div>
      </div>
    </div>
  `;
}

function carteDemandeEnvoyee(d) {
  const mapStatut = {
    attente: { classe: 'badge--alerte',  texte: 'En attente',  indic: 'attente' },
    accepte: { classe: 'badge--succes',  texte: 'Acceptée',    indic: 'accepte' },
    refuse:  { classe: 'badge--danger',  texte: 'Refusée',     indic: 'refuse'  },
  };
  const st = mapStatut[d.statut] || mapStatut.attente;

  return `
    <div class="demande-carte" data-id="${d.id}">
      <div class="demande-indicateur demande-indicateur--${st.indic}"></div>
      <div class="avatar avatar--md avatar--${d.couleur}">${d.initiales}</div>
      <div class="demande-corps">
        <div class="demande-entete">
          <div>
            <div class="demande-nom">${d.nom}</div>
            <div class="demande-meta">${d.filiere}</div>
          </div>
          <div class="flex items-centre gap-2">
            <span class="badge ${st.classe}">${st.texte}</span>
            <span class="demande-date">${d.date}</span>
          </div>
        </div>
        <div class="demande-message">"${d.message}"</div>
        ${d.statut === 'attente' ? `<div class="demande-actions"><button class="btn btn--danger btn--sm" onclick="annulerDemande(${d.id})">Annuler la demande</button></div>` : ''}
        ${d.statut === 'accepte' ? `<div class="demande-actions"><button class="btn btn--primaire btn--sm" onclick="window.location.href='messages.html'">Ouvrir la messagerie</button></div>` : ''}
      </div>
    </div>
  `;
}

function carteDemandeTerminee(d) {
  const etoiles = Array.from({ length: 5 }, function (_, i) {
    return i < d.note ? '★' : '☆';
  }).join('');

  return `
    <div class="demande-carte" data-id="${d.id}">
      <div class="demande-indicateur demande-indicateur--termine"></div>
      <div class="avatar avatar--md avatar--${d.couleur}">${d.initiales}</div>
      <div class="demande-corps">
        <div class="demande-entete">
          <div>
            <div class="demande-nom">${d.nom}</div>
            <div class="demande-meta">${d.filiere}</div>
          </div>
          <div class="flex items-centre gap-2">
            <span class="badge badge--neutre">Terminée</span>
            <span class="demande-date">${d.date}</span>
          </div>
        </div>
        <div class="demande-message">"${d.message}"</div>
        <div class="flex items-centre gap-3">
          <span style="color: var(--alerte); font-size: 1.125rem; letter-spacing:2px;">${etoiles}</span>
          <span class="texte-discret taille-sm">${d.note}/5</span>
        </div>
      </div>
    </div>
  `;
}

/*État vide */
function etatVide(titre, desc) {
  return `
    <div class="etat-vide">
      <div class="etat-vide-titre">${titre}</div>
      <div class="etat-vide-description">${desc}</div>
    </div>
  `;
}

/* ACTIONS*/

function accepterDemande(id) {
  const carte = document.querySelector(`.demande-carte[data-id="${id}"]`);
  if (carte) carte.style.opacity = '0.5';
  afficherToast('Demande acceptée. Un message a été envoyé.', 'succes');
  setTimeout(function () { if (carte) carte.remove(); }, 600);
}

function refuserDemande(id) {
  const carte = document.querySelector(`.demande-carte[data-id="${id}"]`);
  if (carte) carte.style.opacity = '0.5';
  afficherToast('Demande refusée.', 'info');
  setTimeout(function () { if (carte) carte.remove(); }, 600);
}

function annulerDemande(id) {
  const carte = document.querySelector(`.demande-carte[data-id="${id}"]`);
  if (carte) carte.style.opacity = '0.5';
  afficherToast('Demande annulée.', 'info');
  setTimeout(function () { if (carte) carte.remove(); }, 600);
}

function voirProfil(nom) {
  afficherToast(`Profil de ${nom}`, 'info');
}

window.accepterDemande = accepterDemande;
window.refuserDemande  = refuserDemande;
window.annulerDemande  = annulerDemande;
window.voirProfil      = voirProfil;