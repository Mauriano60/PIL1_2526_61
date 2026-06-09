/* ============================================================
   offres.js — Logique de la page Offres IFRI_MentorLink
   Gère : données des offres, affichage des cartes,
          filtrage dynamique, modal de publication
   ============================================================ */

/* ============================================================
   DONNÉES : Liste des offres disponibles
   Dans une vraie application, ces données viendraient d'une API
   ============================================================ */

/* Tableau d'objets représentant chaque offre de mentorat */
const offres = [
  {
    id: 1,                              /* Identifiant unique de l'offre */
    initiales: 'MH',                    /* Initiales du mentor (pour l'avatar) */
    avatarClass: '',                     /* Classe CSS de couleur de l'avatar (bleu par défaut) */
    nom: 'Marie Houngbédji',            /* Nom complet du mentor */
    filiere: 'Génie Logiciel',          /* Filière du mentor */
    filiereCode: 'gl',                  /* Code filière pour le filtrage */
    niveau: 'M1',                       /* Niveau d'études */
    match: 94,                          /* Pourcentage de compatibilité */
    matiere: 'Python',                  /* Matière proposée */
    matiereCode: 'python',              /* Code matière pour le filtrage */
    matiereClass: 'matiere-python',     /* Classe CSS de la couleur du badge matière */
    description: 'Aide au débogage Python, introduction aux librairies Pandas et NumPy. Je propose 2h de session par semaine.',
    /* Description de l'offre */
    disponibilites: [                   /* Tableau des créneaux de disponibilité */
      { jour: 'Mardi', debut: '17:00', fin: '21:00', jourCode: 'mardi' },
      { jour: 'Jeudi', debut: '18:00', fin: '21:00', jourCode: 'jeudi' },
      { jour: 'Samedi', debut: '08:00', fin: '12:00', jourCode: 'samedi' }
    ]
  },
  {
    id: 2,
    initiales: 'PA',
    avatarClass: 'avatar-purple',        /* Violet */
    nom: 'Paul Adéoti',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'L3',
    match: 87,
    matiere: 'SQL',
    matiereCode: 'sql',
    matiereClass: 'matiere-sql',
    description: 'Modélisation de bases de données, requêtes complexes et optimisation.',
    disponibilites: [
      { jour: 'Lundi', debut: '18:00', fin: '21:00', jourCode: 'lundi' },
      { jour: 'Mercredi', debut: '18:00', fin: '21:00', jourCode: 'mercredi' }
    ]
  },
  {
    id: 3,
    initiales: 'AK',
    avatarClass: 'avatar-teal',          /* Vert-bleu */
    nom: 'Aminata Kora',
    filiere: 'SI',
    filiereCode: 'si',
    niveau: 'M2',
    match: null,                         /* null = pas de badge Match affiché */
    matiere: 'Développement Web',
    matiereCode: 'dev-web',
    matiereClass: 'matiere-devweb',
    description: 'React, Node.js et intégration d\'API. Parfait pour les projets de fin d\'année.',
    disponibilites: [
      { jour: 'Samedi', debut: '10:00', fin: '18:00', jourCode: 'samedi' },
      { jour: 'Dimanche', debut: '10:00', fin: '18:00', jourCode: 'dimanche' }
    ]
  },
  {
    id: 4,
    initiales: 'KM',
    avatarClass: 'avatar-indigo',        /* Indigo */
    nom: 'Kofi Mensah',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'L2',
    match: null,
    matiere: 'Algorithmique',
    matiereCode: 'algorithmique',
    matiereClass: 'matiere-algo',
    description: 'Structures de données, complexité, arbres et graphes.',
    disponibilites: [
      { jour: 'Mercredi', debut: '14:00', fin: '18:00', jourCode: 'mercredi' }
    ]
  },
  {
    id: 5,
    initiales: 'FD',
    avatarClass: 'avatar-rose',          /* Rose */
    nom: 'Fatoumata Diallo',
    filiere: 'SI',
    filiereCode: 'si',
    niveau: 'L3',
    match: null,
    matiere: 'Base de données',
    matiereCode: 'bdd',
    matiereClass: 'matiere-bdd',
    description: 'Création et gestion de BDD avec PostgreSQL et MySQL.',
    disponibilites: [
      { jour: 'Jeudi', debut: '18:00', fin: '21:00', jourCode: 'jeudi' }
    ]
  },
  {
    id: 6,
    initiales: 'IT',
    avatarClass: 'avatar-amber',         /* Ambre */
    nom: 'Ibrahim Touré',
    filiere: 'RT',
    filiereCode: 'sr',
    niveau: 'M1',
    match: null,
    matiere: 'Réseaux',
    matiereCode: 'reseaux',
    matiereClass: 'matiere-reseaux',
    description: 'Configuration routeurs Cisco, modèle OSI, TCP/IP approfondi.',
    disponibilites: [
      { jour: 'Samedi', debut: '09:00', fin: '17:00', jourCode: 'samedi' },
      { jour: 'Dimanche', debut: '09:00', fin: '17:00', jourCode: 'dimanche' }
    ]
  }
];

/* ============================================================
   INITIALISATION AU CHARGEMENT DU DOM
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  /* Attend que le HTML soit entièrement chargé */

  afficherOffres(offres); /* Affiche toutes les offres au démarrage */

  console.log('IFRI_MentorLink — Page Offres chargée avec succès.');
});

/* ============================================================
   GÉNÉRATION DES CARTES D'OFFRES
   ============================================================ */

/**
 * Génère et injecte les cartes d'offres dans la grille HTML.
 *
 * @param {Array} listeOffres - Tableau d'objets offre à afficher
 */
function afficherOffres(listeOffres) {

  /* Récupère le conteneur de la grille */
  const grille = document.getElementById('grilleOffres');

  /* Récupère le titre du nombre d'offres */
  const titre = document.getElementById('titreOffres');

  /* Récupère le message "aucun résultat" */
  const aucunResultat = document.getElementById('aucunResultat');

  /* Met à jour le titre avec le nombre d'offres filtrées */
  titre.textContent = `${listeOffres.length} offre${listeOffres.length > 1 ? 's' : ''} disponible${listeOffres.length > 1 ? 's' : ''}`;
  /* Pluriel automatique selon le nombre */

  /* Vide la grille avant de la remplir à nouveau */
  grille.innerHTML = '';

  /* Affiche ou cache le message "aucun résultat" */
  if (listeOffres.length === 0) {
    aucunResultat.classList.remove('d-none'); /* Affiche le message */
    return; /* Arrête la fonction, rien à générer */
  } else {
    aucunResultat.classList.add('d-none'); /* Cache le message */
  }

  /* Boucle sur chaque offre pour créer sa carte HTML */
  listeOffres.forEach(function (offre) {

    /* ---- Génère le badge "Match XX%" si applicable ---- */
    const badgeMatch = offre.match
      ? `<span class="badge-match">Match ${offre.match}%</span>`
      : ''; /* Chaîne vide si pas de match */

    /* ---- Génère les lignes de disponibilités ---- */
    const lignesDispos = offre.disponibilites.length > 0
      ? offre.disponibilites
          .map(function (dispo) {
            return `<div class="dispo-item">${dispo.jour} : ${dispo.debut} - ${dispo.fin}</div>`;
          })
          .join('')
      : `<div class="dispo-item" style="font-style:italic;">Aucune disponibilité renseignée</div>`;

    /* ---- Construit le HTML complet de la carte ---- */
    const carteHTML = `
      <div class="col-md-6 col-lg-4">
        <!-- Colonne Bootstrap : 1/3 sur grand écran, 1/2 sur moyen, pleine sur mobile -->

        <div class="offre-card" data-id="${offre.id}">
          <!-- data-id : référence l'offre pour les actions -->

          <!-- En-tête : infos mentor + badge match -->
          <div class="card-header-row">

            <!-- Avatar + Nom + Filière/Niveau -->
            <div class="card-user-info">

              <!-- Avatar avec initiales -->
              <div class="card-avatar ${offre.avatarClass}">
                ${offre.initiales}
              </div>

              <!-- Nom + badges méta -->
              <div>
                <div class="card-name">${offre.nom}</div>
                <!-- Nom du mentor -->

                <div class="card-meta">
                  <span class="badge-meta">${offre.filiere}</span>
                  <!-- Filière -->
                  <span class="badge-meta">${offre.niveau}</span>
                  <!-- Niveau -->
                </div>
              </div>
            </div>

            <!-- Badge de matching (si disponible) -->
            ${badgeMatch}
          </div>
          <!-- Fin en-tête -->

          <!-- Badge de la matière (ex: PYTHON) -->
          <div>
            <span class="badge-matiere ${offre.matiereClass}">
              ${offre.matiere.toUpperCase()}
              <!-- Majuscules pour le badge matière -->
            </span>
          </div>

          <!-- Description de l'offre -->
          <p class="card-description">${offre.description}</p>

          <!-- Section disponibilités -->
          <div class="card-dispos">

            <!-- Titre avec icône horloge -->
            <div class="dispos-title">
              <i class="bi bi-clock"></i>
              <!-- Icône horloge Bootstrap Icons -->
              <span>Disponibilités</span>
            </div>

            <!-- Lignes de créneaux horaires -->
            ${lignesDispos}
          </div>

          <!-- Boutons d'action -->
          <div class="card-actions">

            <!-- Bouton Voir Profil -->
            <button
              class="btn-voir-profil"
              onclick="voirProfil(${offre.id})"
            >
              Voir Profil
            </button>

            <!-- Bouton Contacter -->
            <button
              class="btn-contacter"
              onclick="contacter(${offre.id})"
            >
              Contacter
            </button>
          </div>

        </div>
        <!-- Fin offre-card -->

      </div>
      <!-- Fin col -->
    `;

    /* Injecte la carte dans la grille */
    grille.insertAdjacentHTML('beforeend', carteHTML);
    /* insertAdjacentHTML('beforeend') : ajoute le HTML comme dernier enfant */
  });
}

/* ============================================================
   FILTRAGE DYNAMIQUE DES OFFRES
   ============================================================ */

/**
 * Filtre les offres selon les valeurs des contrôles de filtre.
 * Appelée à chaque modification d'un filtre (oninput / onchange).
 */
function filtrerOffres() {

  /* ---- Récupère les valeurs de chaque filtre ---- */

  /* Texte de la barre de recherche (minuscules pour comparaison insensible à la casse) */
  const texte = document.getElementById('rechercheOffre').value.toLowerCase().trim();

  /* Code matière sélectionné (ex: 'python', '' = toutes) */
  const matiere = document.getElementById('filtreMatiere').value;

  /* Code filière sélectionné (ex: 'gl', '' = toutes) */
  const filiere = document.getElementById('filtreFiliere').value;

  /* Niveau sélectionné (ex: 'M1', '' = tous) */
  const niveau = document.getElementById('filtreNiveau').value;

  /* Jour sélectionné (ex: 'lundi', '' = tous) */
  const jour = document.getElementById('filtreJour').value;

  /* Heure de début (ex: '17:00', '' = toutes) */
  const heureDebut = document.getElementById('heureDebut').value;

  /* Heure de fin (ex: '21:00', '' = toutes) */
  const heureFin = document.getElementById('heureFin').value;

  /* ---- Filtre le tableau des offres ---- */
  const offresFiltrees = offres.filter(function (offre) {

    /* --- Filtre par texte (nom du mentor ou matière) --- */
    const matchTexte = texte === '' || /* Pas de texte saisi → toutes les offres */
      offre.nom.toLowerCase().includes(texte) ||
      offre.matiere.toLowerCase().includes(texte) ||
      offre.description.toLowerCase().includes(texte);
    /* includes() : vérifie si la chaîne contient le texte recherché */

    /* --- Filtre par matière --- */
    const matchMatiere = matiere === '' || offre.matiereCode === matiere;
    /* Si aucune matière sélectionnée, toutes passent */

    /* --- Filtre par filière --- */
    const matchFiliere = filiere === '' || offre.filiereCode === filiere;
    /* Si aucune filière sélectionnée, toutes passent */

    /* --- Filtre par niveau --- */
    const matchNiveau = niveau === '' || offre.niveau === niveau;
    /* Si aucun niveau sélectionné, tous passent */

    /* --- Filtre par jour de disponibilité --- */
    const matchJour = jour === '' ||
      offre.disponibilites.some(function (dispo) {
        return dispo.jourCode === jour;
        /* some() : retourne true si au moins un créneau correspond au jour */
      });

    /* --- Filtre par heure de début --- */
    const matchHeureDebut = heureDebut === '' ||
      offre.disponibilites.some(function (dispo) {
        return dispo.debut <= heureDebut;
        /* Compare les chaînes d'heure (format HH:MM, comparaison lexicographique) */
      });

    /* --- Filtre par heure de fin --- */
    const matchHeureFin = heureFin === '' ||
      offre.disponibilites.some(function (dispo) {
        return dispo.fin >= heureFin;
        /* Vérifie si la fin du créneau est après l'heure de fin filtrée */
      });

    /* L'offre est incluse seulement si TOUS les filtres correspondent */
    return matchTexte && matchMatiere && matchFiliere && matchNiveau && matchJour && matchHeureDebut && matchHeureFin;
  });

  /* Réaffiche les offres filtrées */
  afficherOffres(offresFiltrees);
}

/* ============================================================
   MODAL : Publier une offre
   ============================================================ */

/**
 * Ouvre le modal Bootstrap de publication d'une offre.
 */
function ouvrirModalPublier() {

  /* Récupère l'élément modal du DOM */
  const modal = document.getElementById('modalPublier');

  /* Crée une instance Bootstrap Modal et l'affiche */
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show(); /* Affiche le modal avec animation Bootstrap */
}

/**
 * Valide et traite la publication d'une nouvelle offre.
 * Appelée au clic sur le bouton "Publier" dans le modal.
 */
function publierOffre() {

  /* ---- Récupère les valeurs des champs du modal ---- */

  const titre   = document.getElementById('modalTitre').value.trim();       /* Titre de l'offre */
  const format  = document.getElementById('modalFormat').value;             /* Format de l'offre */
  const compet  = document.getElementById('modalMatiere').value;            /* Compétence/Matière (id correct : modalMatiere) */
  const desc    = document.getElementById('modalDescription').value.trim(); /* Description */

  /* ---- Validation : tous les champs obligatoires ---- */
  if (!titre || !compet || !format || !desc) {
    alert('Veuillez remplir tous les champs avant de publier.');
    return; /* Arrête la fonction */
  }

  /* Dictionnaire : code matière → libellé lisible */
  const labelsMatiere = {
    'python': 'Python', 'javascript': 'JavaScript', 'sql': 'SQL',
    'dev-web': 'Développement Web', 'algorithmique': 'Algorithmique',
    'bdd': 'Base de données', 'reseaux': 'Réseaux', 'ia/mlrn': 'IA / Machine Learning',
    'si': 'Sécurité Informatique'
  };

  /* Dictionnaire : code matière → classe CSS du badge matière */
  const classesMatiere = {
    'python': 'matiere-python', 'javascript': 'matiere-python', 'sql': 'matiere-sql',
    'dev-web': 'matiere-devweb', 'algorithmique': 'matiere-algo',
    'bdd': 'matiere-bdd', 'reseaux': 'matiere-reseaux', 'ia/mlrn': 'matiere-python',
    'si': 'matiere-bdd'
  };

  /* Construit le nouvel objet offre */
  const nouvelleOffre = {
    id: offres.length + 1,                            /* Nouvel ID unique */
    initiales: 'U',                                   /* Initiale utilisateur */
    avatarClass: '',                                  /* Bleu par défaut (pas de classe spéciale) */
    nom: 'Utilisateur',                               /* Nom de l'utilisateur connecté */
    filiere: 'Ma filière',                            /* Filière de l'utilisateur */
    filiereCode: 'gl',                                /* Code filière par défaut */
    niveau: 'M1',                                     /* Niveau par défaut */
    match: null,                                      /* Pas de badge match pour ses propres offres */
    matiere: labelsMatiere[compet] || compet,         /* Libellé lisible de la matière */
    matiereCode: compet,                              /* Code pour le filtrage */
    matiereClass: classesMatiere[compet] || 'matiere-python', /* Classe CSS du badge */
    description: desc,                               /* Description saisie */
    disponibilites: []                               /* Aucune dispo renseignée (ajout via profil) */
  };

  /* Ajoute la nouvelle offre au tableau global */
  offres.push(nouvelleOffre);

  /* Réaffiche toutes les offres avec la nouvelle */
  afficherOffres(offres);

  /* Ferme le modal Bootstrap */
  const modal = document.getElementById('modalPublier');
  const bsModal = bootstrap.Modal.getInstance(modal);
  if (bsModal) bsModal.hide(); /* Cache le modal si l'instance existe */

  /* Remet les champs du modal à zéro */
  document.getElementById('modalTitre').value = '';
  document.getElementById('modalMatiere').value = '';
  document.getElementById('modalDescription').value = '';
  document.getElementById('modalFormat').value = '';

  /* Message de confirmation dans la console */
  console.log('Nouvelle offre publiée :', nouvelleOffre);
}

/* ============================================================
   ACTIONS DES CARTES : Voir Profil + Contacter
   ============================================================ */

/**
 * Affiche le profil d'un mentor.
 * Dans une vraie application, redirige vers sa page de profil.
 *
 * @param {number} id - L'identifiant de l'offre
 */
function voirProfil(id) {

  /* Cherche l'offre correspondante dans le tableau */
  const offre = offres.find(function (o) { return o.id === id; });
  /* find() : retourne le premier élément qui satisfait la condition */

  if (offre) {
    /* Affiche une alerte de démo */
    alert(`Voir le profil de : ${offre.nom}`);
    /* Dans une vraie app : window.location.href = `profil.html?id=${id}`; */
    console.log('Voir profil :', offre);
  }
}

/**
 * Ouvre la messagerie pour contacter un mentor.
 * Dans une vraie application, ouvre le chat ou un formulaire.
 *
 * @param {number} id - L'identifiant de l'offre
 */
function contacter(id) {

  /* Cherche l'offre correspondante */
  const offre = offres.find(function (o) { return o.id === id; });

  if (offre) {
    /* Affiche une alerte de démo */
    alert(`Contacter : ${offre.nom}`);
    /* Dans une vraie app : ouvrir le chat ou envoyer une demande */
    console.log('Contacter :', offre);
  }
}

/* ============================================================
   UTILITAIRE
   ============================================================ */

/**
 * Met en majuscule la première lettre d'une chaîne.
 *
 * @param {string} str - La chaîne à transformer
 * @returns {string} - La chaîne avec première lettre en majuscule
 */
function capitaliser(str) {
  if (!str) return ''; /* Retourne vide si la chaîne est vide */
  return str.charAt(0).toUpperCase() + str.slice(1);
  /* charAt(0).toUpperCase() : première lettre en majuscule */
  /* slice(1) : reste de la chaîne */
}
