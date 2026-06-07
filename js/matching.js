/* matching.js — Logique de la page Matching
   IFRI MentorLink
   Algorithme de scoring et affichage des correspondances*/

'use strict';

/* PROFIL DE L'UTILISATEUR COURANT (base du calcul de matching)
   Dans une vraie app, ces données viennent de la session Django.*/

const MON_PROFIL = {
  filiere:     'gl',          /* Génie Logiciel */
  niveau:      'L1',
  competences: ['python', 'algorithmique'],
  disponibilites: ['mardi', 'jeudi', 'samedi'],
};

/* DONNÉES DES CANDIDATS (viendront de l'API Django)*/

const CANDIDATS = [
  {
    id: 1, initiales: 'MH', couleur: 'bleu',
    nom: 'Marie Houngbédji', filiere: 'Génie Logiciel', filiereCode: 'gl',
    niveau: 'M1',
    competences: ['python', 'algorithmique', 'sql'],
    disponibilites: ['mardi', 'jeudi', 'samedi'],
    matierePrincipale: 'Python', matiereClasse: 'badge-matiere--python',
  },
  {
    id: 2, initiales: 'PA', couleur: 'violet',
    nom: 'Paul Adéoti', filiere: 'Génie Logiciel', filiereCode: 'gl',
    niveau: 'L3',
    competences: ['sql', 'bdd'],
    disponibilites: ['lundi', 'mercredi'],
    matierePrincipale: 'SQL', matiereClasse: 'badge-matiere--sql',
  },
  {
    id: 3, initiales: 'AK', couleur: 'teal',
    nom: 'Aminata Kora', filiere: 'SI', filiereCode: 'si',
    niveau: 'M2',
    competences: ['dev-web', 'javascript'],
    disponibilites: ['samedi', 'dimanche'],
    matierePrincipale: 'Développement Web', matiereClasse: 'badge-matiere--devweb',
  },
  {
    id: 4, initiales: 'KM', couleur: 'indigo',
    nom: 'Kofi Mensah', filiere: 'Génie Logiciel', filiereCode: 'gl',
    niveau: 'L2',
    competences: ['algorithmique', 'python'],
    disponibilites: ['mercredi'],
    matierePrincipale: 'Algorithmique', matiereClasse: 'badge-matiere--algo',
  },
  {
    id: 5, initiales: 'FD', couleur: 'rose',
    nom: 'Fatoumata Diallo', filiere: 'SI', filiereCode: 'si',
    niveau: 'L3',
    competences: ['bdd', 'sql'],
    disponibilites: ['jeudi'],
    matierePrincipale: 'Base de données', matiereClasse: 'badge-matiere--bdd',
  },
  {
    id: 6, initiales: 'IT', couleur: 'ambre',
    nom: 'Ibrahim Touré', filiere: 'RT', filiereCode: 'sr',
    niveau: 'M1',
    competences: ['reseaux'],
    disponibilites: ['samedi', 'dimanche'],
    matierePrincipale: 'Réseaux', matiereClasse: 'badge-matiere--reseaux',
  },
];

/*ALGORITHME DE MATCHING
   3 critères pondérés :
   - Compatibilité des compétences/matières : 50%
   - Compatibilité des horaires             : 30%
   - Proximité filière et niveau            : 20% */

/**
 * Calcule le score de compatibilité entre le profil courant
 * et un candidat. Retourne un objet avec le score total
 * et le détail par critère.
 *
 * @param {Object} candidat
 * @returns {{ total: number, competences: number, horaires: number, proximite: number }}
 */
function calculerScore(candidat) {

  /*Critère 1 : compatibilité des compétences (sur 50)*/
  const competencesCommunes = MON_PROFIL.competences.filter(function (c) {
    return candidat.competences.includes(c);
  }).length;

  const maxPossible = Math.max(MON_PROFIL.competences.length, 1);
  const scoreCompetences = Math.round((competencesCommunes / maxPossible) * 50);

  /*Critère 2 : compatibilité des horaires (sur 30)*/
  const dispoCommune = MON_PROFIL.disponibilites.filter(function (j) {
    return candidat.disponibilites.includes(j);
  }).length;

  const maxDispo = Math.max(MON_PROFIL.disponibilites.length, 1);
  const scoreHoraires = Math.round((dispoCommune / maxDispo) * 30);

  /*Critère 3 : proximité filière et niveau (sur 20) */
  let scoreProximite = 0;

  /* Même filière : +12 points */
  if (candidat.filiereCode === MON_PROFIL.filiere) {
    scoreProximite += 12;
  }

  /* Niveaux proches : tableau ordonné, score selon l'écart */
  const niveaux = ['L1', 'L2', 'L3', 'M1', 'M2'];
  const ecart = Math.abs(
    niveaux.indexOf(candidat.niveau) - niveaux.indexOf(MON_PROFIL.niveau)
  );

  if (ecart === 0) scoreProximite += 8;
  else if (ecart === 1) scoreProximite += 6;
  else if (ecart === 2) scoreProximite += 3;
  /* Écart >= 3 : 0 points de proximité de niveau */

  /*Score total*/
  const total = Math.min(100, scoreCompetences + scoreHoraires + scoreProximite);

  return {
    total,
    competences: scoreCompetences,
    horaires:    scoreHoraires,
    proximite:   scoreProximite,
  };
}

/* INITIALISATION */

/* Tableau enrichi avec les scores calculés */
let matchesAvecScores = [];

document.addEventListener('DOMContentLoaded', function () {

  /* Calcule les scores pour chaque candidat */
  matchesAvecScores = CANDIDATS.map(function (candidat) {
    const score = calculerScore(candidat);
    return Object.assign({}, candidat, { score });
  });

  /* Trie par score décroissant par défaut */
  matchesAvecScores.sort(function (a, b) { return b.score.total - a.score.total; });

  rendreScoring();
  rendreMatches();
  afficherScoreGlobal();
});

/*AFFICHAGE DU SCORE MOYEN GLOBAL*/

function afficherScoreGlobal() {
  const el = document.getElementById('scoreGlobal');
  if (!el || matchesAvecScores.length === 0) return;

  const moyenne = Math.round(
    matchesAvecScores.reduce(function (acc, m) { return acc + m.score.total; }, 0)
    / matchesAvecScores.length
  );

  el.textContent = moyenne + '%';
}

/*RENDU DES CRITÈRES DE SCORING */

function rendreScoring() {
  const grille = document.getElementById('grilleScoring');
  if (!grille) return;

  const criteres = [
    {
      titre: 'Compatibilité des matières',
      desc: 'Compare les compétences et matières du mentor avec les besoins de l\'apprenant.',
      poids: '50%',
    },
    {
      titre: 'Disponibilités communes',
      desc: 'Évalue la superposition des créneaux horaires disponibles entre les deux profils.',
      poids: '30%',
    },
    {
      titre: 'Proximité filière & niveau',
      desc: 'Favorise les mentors de la même filière et des niveaux proches pour plus de pertinence.',
      poids: '20%',
    },
  ];

  grille.innerHTML = criteres.map(function (c) {
    return `
      <div class="scoring-carte">
        <div class="scoring-carte-titre">${c.titre}</div>
        <div class="scoring-carte-desc">${c.desc}</div>
        <span class="scoring-poids">Poids : ${c.poids}</span>
      </div>
    `;
  }).join('');
}

/*RENDU DE LA LISTE DES MATCHES*/

function rendreMatches() {
  const conteneur = document.getElementById('listeMatches');
  const titre     = document.getElementById('titreMatches');
  const tri       = document.getElementById('triMatches')?.value ?? 'score';

  if (!conteneur) return;

  /* Trie selon le critère sélectionné */
  let liste = [...matchesAvecScores];

  if (tri === 'score') {
    liste.sort(function (a, b) { return b.score.total - a.score.total; });
  } else if (tri === 'filiere') {
    liste.sort(function (a, b) { return a.filiere.localeCompare(b.filiere, 'fr'); });
  } else if (tri === 'niveau') {
    const ordre = ['L1','L2','L3','M1','M2'];
    liste.sort(function (a, b) { return ordre.indexOf(a.niveau) - ordre.indexOf(b.niveau); });
  }

  if (titre) {
    titre.textContent = `${liste.length} correspondance${liste.length > 1 ? 's' : ''} trouvée${liste.length > 1 ? 's' : ''}`;
  }

  conteneur.innerHTML = liste.map(function (m) {
    /* Classe du cercle selon le score */
    let classeCercle = 'match-score-cercle--moyen';
    if (m.score.total >= 80) classeCercle = 'match-score-cercle--excellent';
    else if (m.score.total >= 60) classeCercle = 'match-score-cercle--bon';

    return `
      <div class="match-carte">

        <!-- Score en cercle -->
        <div class="match-score-cercle ${classeCercle}">
          ${m.score.total}%
        </div>

        <!-- Infos du mentor -->
        <div class="match-info">
          <div class="match-nom">${m.nom}</div>
          <div class="match-badges">
            <span class="badge badge--meta">${m.filiere}</span>
            <span class="badge badge--meta">${m.niveau}</span>
            <span class="badge-matiere ${m.matiereClasse}">${m.matierePrincipale.toUpperCase()}</span>
          </div>

          <!-- Détail des critères -->
          <div class="match-detail-scoring">
            <div class="match-critere">
              <span class="match-critere-label">Matières</span>
              <span class="match-critere-valeur">${m.score.competences}/50</span>
            </div>
            <div class="match-critere">
              <span class="match-critere-label">Horaires</span>
              <span class="match-critere-valeur">${m.score.horaires}/30</span>
            </div>
            <div class="match-critere">
              <span class="match-critere-label">Proximité</span>
              <span class="match-critere-valeur">${m.score.proximite}/20</span>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="match-actions">
          <button class="btn btn--primaire btn--sm" onclick="contacterMatch('${m.nom}')">Contacter</button>
          <button class="btn btn--secondaire btn--sm" onclick="voirProfilMatch('${m.nom}')">Profil</button>
        </div>

      </div>
    `;
  }).join('');
}

window.rendreMatches = rendreMatches;

function contacterMatch(nom) {
  afficherToast(`Demande envoyée à ${nom}.`, 'succes');
}

function voirProfilMatch(nom) {
  afficherToast(`Profil de ${nom}`, 'info');
}

window.contacterMatch   = contacterMatch;
window.voirProfilMatch  = voirProfilMatch;