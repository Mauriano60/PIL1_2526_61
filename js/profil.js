'use strict';

/* DONNÉES UTILISATEUR SIMULÉES= */

let profilUtilisateur = {
  prenom:    'Utilisateur',
  nom:       '',
  email:     'utilisateur@ifri.uac.bj',
  filiere:   'Génie Logiciel',
  filiereCode: 'gl',
  niveau:    'L1',
  bio:       'Étudiant en L1 Génie Logiciel à l\'IFRI. Passionné par le développement logiciel et l\'algorithmique.',
  initiales: 'U',
  couleurAvatar: 'bleu',
};

const JOURS = ['Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa', 'Di'];
let joursActifs = [1, 3]; /* Index des jours actifs (0 = Lundi) */

const TOUTES_COMPETENCES = [
  { id: 'python',        label: 'Python' },
  { id: 'javascript',    label: 'JavaScript' },
  { id: 'sql',           label: 'SQL' },
  { id: 'dev-web',       label: 'Développement Web' },
  { id: 'algorithmique', label: 'Algorithmique' },
  { id: 'bdd',           label: 'Base de données' },
  { id: 'reseaux',       label: 'Réseaux' },
  { id: 'ia',            label: 'Intelligence Artificielle' },
  { id: 'c',             label: 'Langage C' },
  { id: 'java',          label: 'Java' },
];

let competencesSelectionnees = ['python', 'algorithmique', 'sql'];

const STATS_PROFIL = [
  { valeur: 3,  label: 'Offres publiées' },
  { valeur: 7,  label: 'Matches actifs' },
  { valeur: 12, label: 'Sessions tenues' },
  { valeur: 4,  label: 'Avis reçus' },
];

const MES_OFFRES = [
  { matiere: 'Python', niveau: 'L1–L2', vue: 14, matiereClasse: 'badge-matiere--python' },
  { matiere: 'Algorithmique', niveau: 'L1', vue: 9, matiereClasse: 'badge-matiere--algo' },
];

const COMPLETION = [
  { label: 'Informations personnelles', pourcent: 100 },
  { label: 'Compétences',              pourcent: 80  },
  { label: 'Disponibilités',           pourcent: 60  },
  { label: 'Photo de profil',           pourcent: 0   },
];

/* INITIALISATION */

document.addEventListener('DOMContentLoaded', function () {
  rendreInfosPersonnelles();
  rendreCompetences();
  rendreDispo();
  rendreStats();
  rendreMesOffres();
  rendreCompletion();
  remplirFormulaire();
});

/* INFORMATIONS PERSONNELLES */

function rendreInfosPersonnelles() {
  const conteneur = document.getElementById('infoPersonnelles');
  if (!conteneur) return;

  const infos = [
    { label: 'Prénom',  valeur: profilUtilisateur.prenom },
    { label: 'Nom',     valeur: profilUtilisateur.nom || '—' },
    { label: 'E-mail',  valeur: profilUtilisateur.email },
    { label: 'Filière', valeur: profilUtilisateur.filiere },
    { label: 'Niveau',  valeur: profilUtilisateur.niveau },
  ];

  conteneur.innerHTML = infos.map(function (info) {
    return `
      <div class="info-ligne">
        <span class="info-ligne-label">${info.label}</span>
        <span class="info-ligne-valeur">${info.valeur}</span>
      </div>
    `;
  }).join('');
}

/* COMPÉTENCES */

function rendreCompetences() {
  const conteneur = document.getElementById('listeCompetences');
  if (!conteneur) return;

  if (competencesSelectionnees.length === 0) {
    conteneur.innerHTML = '<p class="texte-discret taille-sm">Aucune compétence ajoutée.</p>';
    return;
  }

  conteneur.innerHTML = competencesSelectionnees.map(function (id) {
    const comp = TOUTES_COMPETENCES.find(function (c) { return c.id === id; });
    return comp
      ? `<span class="competence-tag">${comp.label}</span>`
      : '';
  }).join('');
}

function rendreChoixCompetences() {
  const conteneur = document.getElementById('competencesChoix');
  if (!conteneur) return;

  conteneur.innerHTML = TOUTES_COMPETENCES.map(function (comp) {
    const sel = competencesSelectionnees.includes(comp.id) ? 'selectionne' : '';
    return `
      <div class="competence-choix ${sel}" data-id="${comp.id}" onclick="toggleCompetence('${comp.id}', this)">
        <span class="competence-choix-label">${comp.label}</span>
      </div>
    `;
  }).join('');
}

function toggleCompetence(id, el) {
  el.classList.toggle('selectionne');
}

function sauvegarderCompetences() {
  const selectionnes = document.querySelectorAll('.competence-choix.selectionne');
  competencesSelectionnees = Array.from(selectionnes).map(function (el) {
    return el.dataset.id;
  });
  rendreCompetences();
  fermerModal('modalCompetences');
  afficherToast('Compétences mises à jour.', 'succes');
}

window.sauvegarderCompetences = sauvegarderCompetences;
window.toggleCompetence = toggleCompetence;

/* Lance le rendu des choix à l'ouverture de la modal */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('[data-ouvrir-modal="modalCompetences"]')?.addEventListener('click', function () {
    setTimeout(rendreChoixCompetences, 50);
  });
});

/* DISPONIBILITÉS */

function rendreDispo() {
  const conteneur = document.getElementById('listeDispo');
  if (!conteneur) return;

  conteneur.innerHTML = `
    <div class="dispo-semaine">
      ${JOURS.map(function (j, i) {
        const actif = joursActifs.includes(i) ? 'actif' : '';
        return `
          <div class="dispo-case">
            <span class="dispo-case-label">${j}</span>
            <div class="dispo-case-bloc ${actif}" onclick="toggleJour(${i}, this)" title="${actif ? 'Disponible — cliquer pour désactiver' : 'Indisponible — cliquer pour activer'}"></div>
          </div>
        `;
      }).join('')}
    </div>
    <p class="texte-discret taille-sm">
      ${joursActifs.length} jour${joursActifs.length > 1 ? 's' : ''} de disponibilité activé${joursActifs.length > 1 ? 's' : ''}.
    </p>
  `;
}

function toggleJour(index, el) {
  el.classList.toggle('actif');
  if (joursActifs.includes(index)) {
    joursActifs = joursActifs.filter(function (i) { return i !== index; });
  } else {
    joursActifs.push(index);
  }
  /* Met à jour le texte de résumé */
  const texte = document.querySelector('#listeDispo p');
  if (texte) {
    texte.textContent = `${joursActifs.length} jour${joursActifs.length > 1 ? 's' : ''} de disponibilité activé${joursActifs.length > 1 ? 's' : ''}.`;
  }
}

window.toggleJour = toggleJour;

/* STATISTIQUES */

function rendreStats() {
  const grille = document.getElementById('statsProfilGrille');
  if (!grille) return;

  grille.innerHTML = STATS_PROFIL.map(function (s) {
    return `
      <div class="stat-mini">
        <div class="stat-mini-valeur">${s.valeur}</div>
        <div class="stat-mini-label">${s.label}</div>
      </div>
    `;
  }).join('');
}

/* MES OFFRES PUBLIÉES */

function rendreMesOffres() {
  const conteneur = document.getElementById('mesOffres');
  if (!conteneur) return;

  if (MES_OFFRES.length === 0) {
    conteneur.innerHTML = `
      <div class="etat-vide" style="padding: var(--s8) 0;">
        <div class="etat-vide-titre">Aucune offre publiée</div>
        <div class="etat-vide-description">Publiez votre première offre de mentorat.</div>
        <a href="offres.html" class="btn btn--primaire btn--sm mt-3">Publier une offre</a>
      </div>
    `;
    return;
  }

  conteneur.innerHTML = MES_OFFRES.map(function (offre) {
    return `
      <div class="offre-mini">
        <div class="offre-mini-gauche">
          <span class="badge-matiere ${offre.matiereClasse}">${offre.matiere.toUpperCase()}</span>
          <div>
            <div class="offre-mini-titre">${offre.matiere}</div>
            <div class="offre-mini-meta">Niveau cible : ${offre.niveau} · ${offre.vue} vues</div>
          </div>
        </div>
        <button class="btn btn--ghost btn--sm">Modifier</button>
      </div>
    `;
  }).join('');
}

/* COMPLÉTION DU PROFIL */

function rendreCompletion() {
  const conteneur = document.getElementById('completionProfil');
  if (!conteneur) return;

  const total = COMPLETION.reduce(function (acc, i) { return acc + i.pourcent; }, 0);
  const moyenne = Math.round(total / COMPLETION.length);

  conteneur.innerHTML = `
    <div style="text-align:center; padding: var(--s4) 0 var(--s5) 0;">
      <div style="font-size:2.5rem; font-weight:800; color:var(--bleu-primaire); letter-spacing:-0.05em; line-height:1;">${moyenne}%</div>
      <div class="texte-discret taille-sm mt-2">Profil complété</div>
    </div>
    ${COMPLETION.map(function (item) {
      return `
        <div class="progression-item mb-3">
          <div class="progression-entete flex justify-entre mb-2">
            <span class="taille-sm poids-500">${item.label}</span>
            <span class="taille-sm texte-discret" style="font-family:var(--police-mono)">${item.pourcent}%</span>
          </div>
          <div class="barre-progression-conteneur">
            <div class="barre-progression-remplie ${item.pourcent >= 80 ? 'barre-progression-remplie--succes' : ''}" style="width:${item.pourcent}%"></div>
          </div>
        </div>
      `;
    }).join('')}
  `;
}

/* SAUVEGARDE DU PROFIL */

function remplirFormulaire() {
  const f = profilUtilisateur;
  const set = function (id, v) { const el = document.getElementById(id); if (el) el.value = v; };
  set('editPrenom', f.prenom);
  set('editNom', f.nom);
  set('editEmail', f.email);
  set('editFiliere', f.filiereCode);
  set('editNiveau', f.niveau);
  set('editBio', f.bio);
}

function sauvegarderProfil() {
  const g = function (id) { return document.getElementById(id)?.value.trim() ?? ''; };

  profilUtilisateur.prenom = g('editPrenom') || profilUtilisateur.prenom;
  profilUtilisateur.nom    = g('editNom');
  profilUtilisateur.email  = g('editEmail') || profilUtilisateur.email;
  profilUtilisateur.bio    = g('editBio') || profilUtilisateur.bio;

  /* Met à jour l'affichage */
  const nomEl = document.getElementById('profilNom');
  if (nomEl) {
    nomEl.textContent = [profilUtilisateur.prenom, profilUtilisateur.nom].filter(Boolean).join(' ');
  }

  rendreInfosPersonnelles();
  fermerModal('modalEditerProfil');
  afficherToast('Profil mis à jour avec succès.', 'succes');
}

function modifierAvatar() {
  afficherToast('Fonctionnalité de photo de profil disponible prochainement.', 'info');
}

window.sauvegarderProfil = sauvegarderProfil;
window.modifierAvatar    = modifierAvatar;