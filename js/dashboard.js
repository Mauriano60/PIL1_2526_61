'use strict';

/* DONNÉES SIMULÉES (viendront de l'API Django) */

/* Statistiques globales */
const STATS = [
  { label: 'Offres disponibles', valeur: 24,  variation: '+3 cette semaine',  classe: '' },
  { label: 'Mes demandes',       valeur: 3,   variation: '1 en attente',      classe: 'carte-stat-point--orange' },
  { label: 'Matches actifs',     valeur: 7,   variation: '+2 ce mois',        classe: 'carte-stat-point--vert' },
  { label: 'Messages non lus',   valeur: 5,   variation: 'Dernière : 14h30',  classe: 'carte-stat-point--rouge' },
];

/* Activité récente */
const ACTIVITES = [
  { texte: 'Marie Houngbédji a accepté votre demande de mentorat', heure: 'Il y a 32 min',  couleur: '#10b981' },
  { texte: 'Nouveau message de Paul Adéoti',                       heure: 'Il y a 1h 15',  couleur: '#2563eb' },
  { texte: 'Vous avez publié une offre Python',                    heure: 'Hier à 18:00',  couleur: '#7c3aed' },
  { texte: 'Session de mentorat terminée avec Kofi Mensah',        heure: 'Hier à 16:30',  couleur: '#0d9488' },
  { texte: 'Ibrahim Touré a consulté votre profil',               heure: 'Il y a 2 jours', couleur: '#94a3b8' },
];

/* Mentors suggérés */
const MENTORS_SUGGERES = [
  { initiales: 'MH', nom: 'Marie Houngbédji', meta: 'Génie Logiciel · M1', match: 94, couleur: 'bleu' },
  { initiales: 'AK', nom: 'Aminata Kora',     meta: 'SI · M2',             match: 88, couleur: 'violet' },
  { initiales: 'IT', nom: 'Ibrahim Touré',    meta: 'RT · M1',             match: 81, couleur: 'teal' },
  { initiales: 'KM', nom: 'Kofi Mensah',      meta: 'GL · L2',             match: 76, couleur: 'indigo' },
];

/* Disponibilités de l'utilisateur */
const JOURS_SEMAINE = ['Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa', 'Di'];
const JOURS_ACTIFS  = [1, 3, 5]; /* Index des jours actifs (0-indexed) */

/* Éléments de progression du profil */
const PROGRESSION_ITEMS = [
  { label: 'Informations personnelles', pourcent: 100 },
  { label: 'Compétences et matières',   pourcent: 80  },
  { label: 'Disponibilités',           pourcent: 60  },
  { label: 'Photo de profil',           pourcent: 0   },
];

/* INITIALISATION */

document.addEventListener('DOMContentLoaded', function () {
  rendreStats();
  rendreActivite();
  rendreMentors();
  rendreDispo();
  rendreProgression();
});

/* RENDU DES STATISTIQUES*/

function rendreStats() {
  const grille = document.getElementById('grilleStats');
  if (!grille) return;

  grille.innerHTML = STATS.map(function (stat) {
    return `
      <div class="carte-stat">
        <div class="carte-stat-entete">
          <span class="carte-stat-label">${stat.label}</span>
          <span class="carte-stat-point ${stat.classe}"></span>
        </div>
        <div class="carte-stat-valeur">${stat.valeur}</div>
        <div class="carte-stat-variation">${stat.variation}</div>
      </div>
    `;
  }).join('');
}

/* RENDU DE L'ACTIVITÉ RÉCENTE */

function rendreActivite() {
  const liste = document.getElementById('listeActivite');
  if (!liste) return;

  liste.innerHTML = ACTIVITES.map(function (item) {
    return `
      <div class="activite-item">
        <div class="activite-point" style="background-color: ${item.couleur};"></div>
        <div class="activite-info">
          <div class="activite-texte">${item.texte}</div>
          <div class="activite-heure">${item.heure}</div>
        </div>
      </div>
    `;
  }).join('');
}

/* RENDU DES MENTORS SUGGÉRÉS*/

function rendreMentors() {
  const liste = document.getElementById('listeMentors');
  if (!liste) return;

  liste.innerHTML = MENTORS_SUGGERES.map(function (mentor) {
    return `
      <div class="mentor-item" onclick="window.location.href='offres.html'">
        <div class="avatar avatar--sm avatar--${mentor.couleur}">${mentor.initiales}</div>
        <div class="mentor-item-info">
          <div class="mentor-item-nom">${mentor.nom}</div>
          <div class="mentor-item-meta">${mentor.meta}</div>
        </div>
        <span class="badge badge--match">Match ${mentor.match}%</span>
      </div>
    `;
  }).join('');
}

/*  RENDU DES DISPONIBILITÉS */

function rendreDispo() {
  const grille = document.getElementById('grilleDispo');
  if (!grille) return;

  grille.innerHTML = `
    <div class="dispo-grille">
      ${JOURS_SEMAINE.map(function (jour, i) {
        const actif = JOURS_ACTIFS.includes(i) ? 'actif' : '';
        return `
          <div class="dispo-jour">
            <span class="dispo-jour-label">${jour}</span>
            <div class="dispo-jour-case ${actif}" title="${actif ? 'Disponible' : 'Indisponible'}"></div>
          </div>
        `;
      }).join('')}
    </div>
    <p class="texte-discret taille-sm mt-4">
      ${JOURS_ACTIFS.length} jour${JOURS_ACTIFS.length > 1 ? 's' : ''} de disponibilité configuré${JOURS_ACTIFS.length > 1 ? 's' : ''}.
    </p>
  `;
}

/*  RENDU DE LA PROGRESSION DU PROFIL */

function rendreProgression() {
  const conteneur = document.getElementById('progressionProfil');
  if (!conteneur) return;

  /* Calcule la moyenne de complétion */
  const total = PROGRESSION_ITEMS.reduce(function (acc, item) { return acc + item.pourcent; }, 0);
  const moyenne = Math.round(total / PROGRESSION_ITEMS.length);

  /* Couleur de la barre selon la complétion */
  function classeProgression(p) {
    if (p >= 80) return 'barre-progression-remplie--succes';
    if (p >= 40) return '';
    return 'barre-progression-remplie--alerte';
  }

  conteneur.innerHTML = `
    <div class="score-complet">
      <div class="score-chiffre">${moyenne}%</div>
      <div class="score-label">Profil complété</div>
    </div>

    ${PROGRESSION_ITEMS.map(function (item) {
      return `
        <div class="progression-item">
          <div class="progression-entete">
            <span class="progression-label">${item.label}</span>
            <span class="progression-pourcent">${item.pourcent}%</span>
          </div>
          <div class="barre-progression-conteneur">
            <div
              class="barre-progression-remplie ${classeProgression(item.pourcent)}"
              style="width: ${item.pourcent}%;"
            ></div>
          </div>
        </div>
      `;
    }).join('')}
  `;
}