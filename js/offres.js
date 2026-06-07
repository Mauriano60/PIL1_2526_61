'use strict';

/* DONNÉES DES OFFRES (viendront de l'API Django) */

let offres = [
  {
    id: 1,
    initiales: 'MH',
    couleurAvatar: 'bleu',
    nom: 'Marie Houngbédji',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'M1',
    match: 94,
    matiere: 'Python',
    matiereCode: 'python',
    matiereClasseBadge: 'badge-matiere--python',
    description: 'Aide au débogage Python, introduction aux librairies Pandas et NumPy pour l\'analyse de données. Sessions de 2h par semaine avec exercices pratiques.',
    disponibilites: [
      { jour: 'Mardi',  debut: '17:00', fin: '21:00', jourCode: 'mardi'  },
      { jour: 'Jeudi',  debut: '18:00', fin: '21:00', jourCode: 'jeudi'  },
      { jour: 'Samedi', debut: '08:00', fin: '12:00', jourCode: 'samedi' }
    ]
  },
  {
    id: 2,
    initiales: 'PA',
    couleurAvatar: 'violet',
    nom: 'Paul Adéoti',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'L3',
    match: 87,
    matiere: 'SQL',
    matiereCode: 'sql',
    matiereClasseBadge: 'badge-matiere--sql',
    description: 'Modélisation de bases de données relationnelles, requêtes complexes et optimisation des performances. Idéal pour les projets de BDD.',
    disponibilites: [
      { jour: 'Lundi',    debut: '18:00', fin: '21:00', jourCode: 'lundi'    },
      { jour: 'Mercredi', debut: '18:00', fin: '21:00', jourCode: 'mercredi' }
    ]
  },
  {
    id: 3,
    initiales: 'AK',
    couleurAvatar: 'teal',
    nom: 'Aminata Kora',
    filiere: 'SI',
    filiereCode: 'si',
    niveau: 'M2',
    match: null,
    matiere: 'Développement Web',
    matiereCode: 'dev-web',
    matiereClasseBadge: 'badge-matiere--devweb',
    description: 'React, Node.js et intégration d\'API REST. Parfait pour les projets de fin d\'année. Approche par projets concrets.',
    disponibilites: [
      { jour: 'Samedi',  debut: '10:00', fin: '18:00', jourCode: 'samedi'  },
      { jour: 'Dimanche', debut: '10:00', fin: '18:00', jourCode: 'dimanche' }
    ]
  },
  {
    id: 4,
    initiales: 'KM',
    couleurAvatar: 'indigo',
    nom: 'Kofi Mensah',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'L2',
    match: null,
    matiere: 'Algorithmique',
    matiereCode: 'algorithmique',
    matiereClasseBadge: 'badge-matiere--algo',
    description: 'Structures de données, analyse de complexité algorithmique, arbres et graphes. Méthodes de résolution de problèmes pour concours.',
    disponibilites: [
      { jour: 'Mercredi', debut: '14:00', fin: '18:00', jourCode: 'mercredi' }
    ]
  },
  {
    id: 5,
    initiales: 'FD',
    couleurAvatar: 'rose',
    nom: 'Fatoumata Diallo',
    filiere: 'SI',
    filiereCode: 'si',
    niveau: 'L3',
    match: null,
    matiere: 'Base de données',
    matiereCode: 'bdd',
    matiereClasseBadge: 'badge-matiere--bdd',
    description: 'Création et gestion de bases de données avec PostgreSQL et MySQL. Conception de schémas relationnels et optimisation.',
    disponibilites: [
      { jour: 'Jeudi', debut: '18:00', fin: '21:00', jourCode: 'jeudi' }
    ]
  },
  {
    id: 6,
    initiales: 'IT',
    couleurAvatar: 'ambre',
    nom: 'Ibrahim Touré',
    filiere: 'RT',
    filiereCode: 'sr',
    niveau: 'M1',
    match: null,
    matiere: 'Réseaux',
    matiereCode: 'reseaux',
    matiereClasseBadge: 'badge-matiere--reseaux',
    description: 'Configuration de routeurs Cisco, modèle OSI, protocoles TCP/IP. Préparation aux certifications réseau.',
    disponibilites: [
      { jour: 'Samedi',  debut: '09:00', fin: '17:00', jourCode: 'samedi'  },
      { jour: 'Dimanche', debut: '09:00', fin: '17:00', jourCode: 'dimanche' }
    ]
  }
];

/* INITIALISATION */

document.addEventListener('DOMContentLoaded', function () {
  afficherOffres(offres);
});

/* GÉNÉRATION ET AFFICHAGE DES CARTES */

/**
 * Génère et injecte les cartes d'offres dans la grille.
 * @param {Array} liste - Tableau d'objets offre à afficher
 */
function afficherOffres(liste) {

  const grille        = document.getElementById('grilleOffres');
  const titre         = document.getElementById('titreOffres');
  const aucunResultat = document.getElementById('aucunResultat');

  if (!grille) return;

  /* Met à jour le titre avec le nombre de résultats */
  if (titre) {
    const n = liste.length;
    titre.textContent = `${n} offre${n > 1 ? 's' : ''} disponible${n > 1 ? 's' : ''}`;
  }

  /* Vide la grille */
  grille.innerHTML = '';

  /* Affiche ou cache le message "aucun résultat" */
  if (liste.length === 0) {
    aucunResultat.classList.remove('cache');
    return;
  }
  aucunResultat.classList.add('cache');

  /* Génère chaque carte */
  liste.forEach(function (offre) {

    /* Badge "Match XX%" — uniquement si score défini */
    const htmlBadgeMatch = offre.match
      ? `<span class="badge badge--match">Match ${offre.match}%</span>`
      : '';

    /* Lignes de disponibilités */
    const htmlCreneaux = offre.disponibilites
      .map(function (d) {
        return `<div class="offre-carte-creneau">${d.jour} · ${d.debut} – ${d.fin}</div>`;
      })
      .join('');

    /* HTML de la carte */
    const html = `
      <div class="offre-carte" data-id="${offre.id}">

        <!-- En-tête : avatar + nom + match -->
        <div class="offre-carte-entete">
          <div class="offre-carte-mentor">
            <div class="avatar avatar--md avatar--${offre.couleurAvatar}">
              ${offre.initiales}
            </div>
            <div style="min-width:0">
              <div class="offre-carte-nom">${offre.nom}</div>
              <div class="offre-carte-badges-meta">
                <span class="badge badge--meta">${offre.filiere}</span>
                <span class="badge badge--meta">${offre.niveau}</span>
              </div>
            </div>
          </div>
          ${htmlBadgeMatch}
        </div>

        <!-- Badge matière -->
        <div class="offre-carte-matiere">
          <span class="badge-matiere ${offre.matiereClasseBadge}">
            ${offre.matiere.toUpperCase()}
          </span>
        </div>

        <!-- Description -->
        <p class="offre-carte-description">${offre.description}</p>

        <!-- Disponibilités -->
        <div class="offre-carte-dispos">
          <div class="offre-carte-dispos-titre">Disponibilités</div>
          ${htmlCreneaux}
        </div>

        <!-- Séparateur -->
        <hr class="offre-carte-separateur" />

        <!-- Boutons d'action -->
        <div class="offre-carte-actions">
          <button class="btn btn--secondaire btn--sm" onclick="voirProfil(${offre.id})">
            Voir le profil
          </button>
          <button class="btn btn--primaire btn--sm" onclick="contacter(${offre.id})">
            Contacter
          </button>
        </div>

      </div>
    `;

    grille.insertAdjacentHTML('beforeend', html);
  });
}

/* FILTRAGE DYNAMIQUE */

/**
 * Filtre les offres selon tous les critères actifs.
 * Appelée à chaque interaction avec les contrôles de filtre.
 */
function filtrerOffres() {

  /* Récupère les valeurs de chaque filtre */
  const texte     = document.getElementById('rechercheOffre')?.value.toLowerCase().trim() ?? '';
  const matiere   = document.getElementById('filtreMatiere')?.value ?? '';
  const filiere   = document.getElementById('filtreFiliere')?.value ?? '';
  const niveau    = document.getElementById('filtreNiveau')?.value ?? '';
  const jour      = document.getElementById('filtreJour')?.value ?? '';
  const debutFil  = document.getElementById('heureDebut')?.value ?? '';
  const finFil    = document.getElementById('heureFin')?.value ?? '';
  const tri       = document.getElementById('triOffres')?.value ?? 'match';

  /* Filtre le tableau */
  let resultat = offres.filter(function (offre) {

    /* Filtre texte libre */
    const matchTexte = texte === ''
      || offre.nom.toLowerCase().includes(texte)
      || offre.matiere.toLowerCase().includes(texte)
      || offre.description.toLowerCase().includes(texte);

    /* Filtre par matière */
    const matchMatiere = matiere === '' || offre.matiereCode === matiere;

    /* Filtre par filière */
    const matchFiliere = filiere === '' || offre.filiereCode === filiere;

    /* Filtre par niveau */
    const matchNiveau = niveau === '' || offre.niveau === niveau;

    /* Filtre par jour — au moins un créneau doit correspondre */
    const matchJour = jour === ''
      || offre.disponibilites.some(function (d) { return d.jourCode === jour; });

    /* Filtre par heure de début — comparaison lexicographique HH:MM */
    const matchDebut = debutFil === ''
      || offre.disponibilites.some(function (d) { return d.debut <= debutFil; });

    /* Filtre par heure de fin */
    const matchFin = finFil === ''
      || offre.disponibilites.some(function (d) { return d.fin >= finFil; });

    return matchTexte && matchMatiere && matchFiliere && matchNiveau
        && matchJour  && matchDebut   && matchFin;
  });

  /* Tri des résultats */
  if (tri === 'match') {
    /* Les offres avec match en premier (descendant), puis les autres */
    resultat.sort(function (a, b) {
      if (a.match === null && b.match === null) return 0;
      if (a.match === null) return 1;
      if (b.match === null) return -1;
      return b.match - a.match;
    });
  } else if (tri === 'nom') {
    resultat.sort(function (a, b) { return a.nom.localeCompare(b.nom, 'fr'); });
  }
  /* 'recent' : ordre d'insertion du tableau (défaut) */

  afficherOffres(resultat);
}

/**
 * Réinitialise tous les filtres et réaffiche toutes les offres.
 */
function reinitialiserFiltres() {
  const ids = ['rechercheOffre', 'filtreMatiere', 'filtreFiliere', 'filtreNiveau', 'filtreJour', 'heureDebut', 'heureFin'];
  ids.forEach(function (id) {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  afficherOffres(offres);
}

window.reinitialiserFiltres = reinitialiserFiltres;
window.filtrerOffres = filtrerOffres;

/* MODAL : PUBLICATION D'UNE OFFRE */

/**
 * Valide et traite la publication d'une nouvelle offre.
 * Dans une vraie app : POST /api/offres/
 */
function publierOffre() {

  /* Récupère les valeurs du formulaire */
  const matiere    = document.getElementById('modalMatiere').value;
  const desc       = document.getElementById('modalDescription').value.trim();
  const jour       = document.getElementById('modalJour').value;
  const heureDebut = document.getElementById('modalHeureDebut').value;
  const heureFin   = document.getElementById('modalHeureFin').value;

  /* Validation */
  if (!matiere || !desc || !jour || !heureDebut || !heureFin) {
    afficherToast('Veuillez remplir tous les champs avant de publier.', 'erreur');
    return;
  }

  if (heureDebut >= heureFin) {
    afficherToast('L\'heure de fin doit être après l\'heure de début.', 'erreur');
    return;
  }

  /* Correspondance matière → classe de badge */
  const mapBadge = {
    python: 'badge-matiere--python',
    sql: 'badge-matiere--sql',
    'dev-web': 'badge-matiere--devweb',
    algorithmique: 'badge-matiere--algo',
    bdd: 'badge-matiere--bdd',
    reseaux: 'badge-matiere--reseaux',
    ia: 'badge-matiere--ia',
    javascript: 'badge-matiere--devweb',
  };

  /* Libellés lisibles pour matière et jour */
  const libelleMatiere = document.getElementById('modalMatiere').options[document.getElementById('modalMatiere').selectedIndex].text;
  const libelleJour    = document.getElementById('modalJour').options[document.getElementById('modalJour').selectedIndex].text;

  /* Construit le nouvel objet offre */
  const nouvelleOffre = {
    id:              offres.length + 1,
    initiales:       'U',
    couleurAvatar:   'bleu',
    nom:             'Utilisateur',
    filiere:         'Mon équipe',
    filiereCode:     'gl',
    niveau:          'L1',
    match:           null,
    matiere:         libelleMatiere,
    matiereCode:     matiere,
    matiereClasseBadge: mapBadge[matiere] || 'badge-matiere--algo',
    description:     desc,
    disponibilites: [{
      jour:     libelleJour,
      debut:    heureDebut,
      fin:      heureFin,
      jourCode: jour
    }]
  };

  /* Ajoute au tableau global */
  offres.push(nouvelleOffre);

  /* Réaffiche toutes les offres */
  afficherOffres(offres);

  /* Ferme la modal et réinitialise le formulaire */
  fermerModal('modalPublier');
  document.getElementById('modalMatiere').value      = '';
  document.getElementById('modalDescription').value  = '';
  document.getElementById('modalJour').value         = '';
  document.getElementById('modalHeureDebut').value   = '';
  document.getElementById('modalHeureFin').value     = '';

  afficherToast('Votre offre a été publiée avec succès.', 'succes');
}

window.publierOffre = publierOffre;

/* ACTIONS DES CARTES */

/**
 * Navigue vers le profil d'un mentor.
 * Dans une vraie app : window.location.href = `profil.html?id=${id}`
 * @param {number} id
 */
function voirProfil(id) {
  const offre = offres.find(function (o) { return o.id === id; });
  if (offre) {
    /* Simule une navigation */
    afficherToast(`Profil de ${offre.nom}`, 'info');
  }
}

/**
 * Ouvre la messagerie pour contacter un mentor.
 * Dans une vraie app : redirection vers messages.html?mentorId=${id}
 * @param {number} id
 */
function contacter(id) {
  const offre = offres.find(function (o) { return o.id === id; });
  if (offre) {
    afficherToast(`Demande envoyée à ${offre.nom}`, 'succes');
  }
}

window.voirProfil = voirProfil;
window.contacter  = contacter;