/* ============================================================
   demandes.js — Logique JavaScript de la page Demandes
   Fonctionnalités :
     - Données des demandes et des offres disponibles
     - Génération dynamique des cartes de demandes
     - Filtrage en temps réel (matière, filière, niveau, jour, heure)
     - Publication d'une nouvelle demande (modal avec Matière, Format, Lacunes)
     - Affichage des offres correspondantes à une demande
     - Bouton Accepter une offre qui correspond
   ============================================================ */

/* ============================================================
   DONNÉES : Offres disponibles sur la plateforme
   Reprises de offres.js pour le matching avec les demandes
   ============================================================ */

/* Tableau des offres disponibles (même structure que dans offres.js) */
const offresDisponibles = [
  {
    id: 1,
    initiales: 'MH',
    avatarClass: 'avatar-bleu',       /* Bleu */
    nom: 'Marie Houngbédji',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'M1',
    matiere: 'Python',
    matiereCode: 'python',            /* Code pour le matching */
    description: 'Aide au débogage Python, introduction aux librairies Pandas et NumPy. Je propose 2h de session par semaine.',
    disponibilites: [
      { jour: 'Mardi',  debut: '17:00', fin: '21:00', jourCode: 'mardi'  },
      { jour: 'Jeudi',  debut: '18:00', fin: '21:00', jourCode: 'jeudi'  },
      { jour: 'Samedi', debut: '08:00', fin: '12:00', jourCode: 'samedi' }
    ]
  },
  {
    id: 2,
    initiales: 'PA',
    avatarClass: 'avatar-violet',
    nom: 'Paul Adéoti',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'L3',
    matiere: 'SQL',
    matiereCode: 'sql',
    description: 'Modélisation de bases de données, requêtes complexes et optimisation.',
    disponibilites: [
      { jour: 'Lundi',    debut: '18:00', fin: '21:00', jourCode: 'lundi'    },
      { jour: 'Mercredi', debut: '18:00', fin: '21:00', jourCode: 'mercredi' }
    ]
  },
  {
    id: 3,
    initiales: 'AK',
    avatarClass: 'avatar-teal',
    nom: 'Aminata Kora',
    filiere: 'SI',
    filiereCode: 'si',
    niveau: 'M2',
    matiere: 'Développement Web',
    matiereCode: 'dev-web',
    description: 'React, Node.js et intégration d\'API. Parfait pour les projets de fin d\'année.',
    disponibilites: [
      { jour: 'Samedi',  debut: '10:00', fin: '18:00', jourCode: 'samedi'  },
      { jour: 'Dimanche', debut: '10:00', fin: '18:00', jourCode: 'dimanche' }
    ]
  },
  {
    id: 4,
    initiales: 'KM',
    avatarClass: 'avatar-indigo',
    nom: 'Kofi Mensah',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'L2',
    matiere: 'Algorithmique',
    matiereCode: 'algorithmique',
    description: 'Structures de données, complexité, arbres et graphes.',
    disponibilites: [
      { jour: 'Mercredi', debut: '14:00', fin: '18:00', jourCode: 'mercredi' }
    ]
  },
  {
    id: 5,
    initiales: 'FD',
    avatarClass: 'avatar-rose',
    nom: 'Fatoumata Diallo',
    filiere: 'SI',
    filiereCode: 'si',
    niveau: 'L3',
    matiere: 'Base de données',
    matiereCode: 'bdd',
    description: 'Création et gestion de BDD avec PostgreSQL et MySQL.',
    disponibilites: [
      { jour: 'Jeudi', debut: '18:00', fin: '21:00', jourCode: 'jeudi' }
    ]
  },
  {
    id: 6,
    initiales: 'IT',
    avatarClass: 'avatar-orange',
    nom: 'Ibrahim Touré',
    filiere: 'RT',
    filiereCode: 'sr',
    niveau: 'M1',
    matiere: 'Réseaux',
    matiereCode: 'reseaux',
    description: 'Configuration routeurs Cisco, modèle OSI, TCP/IP approfondi.',
    disponibilites: [
      { jour: 'Samedi',  debut: '09:00', fin: '17:00', jourCode: 'samedi'  },
      { jour: 'Dimanche', debut: '09:00', fin: '17:00', jourCode: 'dimanche' }
    ]
  }
];

/* ============================================================
   DONNÉES : Demandes publiées
   ============================================================ */

/* Tableau d'objets représentant chaque demande de mentorat */
const demandes = [
  {
    id: 1,
    initiales: 'PA',
    avatarClass: 'avatar-violet',      /* Violet */
    nom: 'Paul Adéoti',
    filiere: 'Génie Logiciel',
    filiereCode: 'gl',
    niveau: 'L3',
    urgent: false,                     /* Pas de badge URGENT */
    matiere: 'Algorithmique',
    matiereCode: 'algorithmique',      /* Code pour le filtrage et le matching */
    lacunes: 'algorithmique',          /* Lacune déclarée */
    format: 'presentiel',              /* Format souhaité */
    besoinClass: 'besoin-algorithmique',
    description: 'J\'ai du mal avec les algorithmes de tri et de graphes. J\'aimerais avoir un mentor disponible le soir pour m\'accompagner 1 à 2 fois par semaine.',
    disponibilites: [
      { jour: 'Lundi',    debut: '18:00', fin: '21:00', jourCode: 'lundi'    },
      { jour: 'Mercredi', debut: '18:00', fin: '21:00', jourCode: 'mercredi' },
      { jour: 'Dimanche', debut: '09:00', fin: '17:00', jourCode: 'dimanche' }
    ]
  },
  {
    id: 2,
    initiales: 'AK',
    avatarClass: 'avatar-rose',
    nom: 'Aminata Kora',
    filiere: 'SI',
    filiereCode: 'si',
    niveau: 'L2',
    urgent: true,                      /* Badge URGENT affiché en rouge */
    matiere: 'Réseaux',
    matiereCode: 'reseaux',
    lacunes: 'reseaux',
    format: 'enligne',
    besoinClass: 'besoin-reseaux',
    description: 'Besoin d\'aide pour comprendre le subnetting et les masques de sous-réseaux pour mon examen de la semaine prochaine.',
    disponibilites: [
      { jour: 'Dimanche', debut: '14:00', fin: '18:00', jourCode: 'dimanche' }
    ]
  },
  {
    id: 3,
    initiales: 'KM',
    avatarClass: 'avatar-vert',
    nom: 'Koffi Mensah',
    filiere: 'GL',
    filiereCode: 'gl',
    niveau: 'L1',
    urgent: false,
    matiere: 'Python',
    matiereCode: 'python',
    lacunes: 'python',
    format: 'lesdeux',
    besoinClass: 'besoin-python',
    description: 'Débutant total en programmation. Je cherche quelqu\'un de patient pour m\'expliquer les bases (boucles, fonctions, listes).',
    disponibilites: [
      { jour: 'Lundi',    debut: '17:00', fin: '21:00', jourCode: 'lundi'    },
      { jour: 'Mardi',    debut: '17:00', fin: '21:00', jourCode: 'mardi'    },
      { jour: 'Mercredi', debut: '17:00', fin: '21:00', jourCode: 'mercredi' },
      { jour: 'Samedi',   debut: '10:00', fin: '18:00', jourCode: 'samedi'   },
      { jour: 'Dimanche', debut: '10:00', fin: '18:00', jourCode: 'dimanche' }
    ]
  },
  {
    id: 4,
    initiales: 'FD',
    avatarClass: 'avatar-violet',
    nom: 'Fatou Diallo',
    filiere: 'SI',
    filiereCode: 'si',
    niveau: 'L3',
    urgent: false,
    matiere: 'Base de données',
    matiereCode: 'bdd',
    lacunes: 'bdd',
    format: 'presentiel',
    besoinClass: 'besoin-bdd',
    description: 'Je bloque sur les jointures externes et les sous-requêtes en SQL. Un coup de main serait apprécié !',
    disponibilites: [
      { jour: 'Lundi', debut: '18:30', fin: '21:00', jourCode: 'lundi' },
      { jour: 'Mardi', debut: '18:30', fin: '21:00', jourCode: 'mardi' },
      { jour: 'Jeudi', debut: '18:30', fin: '21:00', jourCode: 'jeudi' }
    ]
  }
];

/* ============================================================
   INITIALISATION AU CHARGEMENT DU DOM
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  /* Attend que tout le HTML soit chargé */

  afficherDemandes(demandes); /* Affiche toutes les demandes au démarrage */

  console.log('IFRI MentorLink — Page Demandes chargée avec succès.');
});

/* ============================================================
   GÉNÉRATION DES CARTES DE DEMANDES
   ============================================================ */

/**
 * Génère et injecte les cartes de demandes dans la grille HTML.
 *
 * @param {Array} listeDemandes - Tableau de demandes à afficher
 */
function afficherDemandes(listeDemandes) {

  /* Récupère la grille, le titre et le bloc "aucun résultat" */
  const grille        = document.getElementById('grilleDemandes');
  const titre         = document.getElementById('titreDemandes');
  const aucunResultat = document.getElementById('aucunResultat');

  /* Met à jour le titre avec le nombre de demandes */
  const nb = listeDemandes.length;
  titre.textContent = `${nb} demande${nb > 1 ? 's' : ''} disponible${nb > 1 ? 's' : ''}`;
  /* Gestion automatique du pluriel */

  /* Vide la grille avant de la reconstruire */
  grille.innerHTML = '';

  /* Affiche ou cache le message "aucun résultat" */
  if (nb === 0) {
    aucunResultat.classList.remove('d-none'); /* Affiche le message */
    return; /* Sort de la fonction */
  }
  aucunResultat.classList.add('d-none'); /* Cache le message */

  /* Boucle sur chaque demande pour générer sa carte */
  listeDemandes.forEach(function (demande) {

    /* Badge URGENT : affiché seulement si demande.urgent === true */
    const badgeUrgent = demande.urgent
      ? `<span class="badge-urgent">URGENT</span>`
      : ''; /* Chaîne vide si pas urgent */

    /* Lignes de disponibilités horaires */
    const lignesDispos = demande.disponibilites
      .map(function (d) {
        return `<div class="dispo-item">${d.jour} : ${d.debut} - ${d.fin}</div>`;
        /* Génère une ligne par créneau */
      })
      .join(''); /* Fusionne toutes les lignes */

    /* HTML complet de la carte */
    const carteHTML = `
      <div class="col-md-6 col-lg-4">
        <!-- col-lg-4 : 3 colonnes sur grand écran, col-md-6 : 2 sur moyen -->

        <div class="demande-card" data-id="${demande.id}">

          <!-- En-tête : avatar + nom + badge urgent -->
          <div class="card-header-row">
            <div class="card-user-info">
              <!-- Avatar avec initiales colorées -->
              <div class="card-avatar ${demande.avatarClass}">${demande.initiales}</div>
              <div>
                <div class="card-name">${demande.nom}</div>
                <!-- Nom de l'étudiant -->
                <div class="card-meta">
                  <span class="badge-meta">${demande.filiere}</span>
                  <!-- Badge filière -->
                  <span class="badge-meta">${demande.niveau}</span>
                  <!-- Badge niveau -->
                </div>
              </div>
            </div>
            ${badgeUrgent}
            <!-- Badge URGENT ou chaîne vide -->
          </div>

          <!-- Badge de matière demandée -->
          <div>
            <span class="badge-besoin ${demande.besoinClass}">
              BESOIN EN : ${demande.matiere.toUpperCase()}
              <!-- toUpperCase() : majuscules pour l'effet visuel -->
            </span>
          </div>

          <!-- Description de la demande -->
          <p class="card-description">${demande.description}</p>

          <!-- Disponibilités -->
          <div class="card-dispos">
            <div class="dispos-title">
              <i class="bi bi-clock"></i>
              <!-- Icône horloge Bootstrap Icons -->
              <span>Disponibilités</span>
            </div>
            ${lignesDispos}
            <!-- Créneaux horaires générés -->
          </div>

          <!-- Boutons d'action -->
          <div class="card-actions">
            <!-- Voir Profil : contour gris -->
            <button class="btn-voir-profil" onclick="voirProfil(${demande.id})">
              Voir Profil
            </button>
            <!-- Voir les offres correspondantes : bleu plein -->
            <button class="btn-voir-offres" onclick="voirOffresCorrespondantes(${demande.id})">
              Voir les offres
              <!-- Ouvre le modal des offres qui matchent cette demande -->
            </button>
          </div>

        </div>
        <!-- Fin demande-card -->
      </div>
    `;

    /* Injecte la carte dans la grille */
    grille.insertAdjacentHTML('beforeend', carteHTML);
    /* insertAdjacentHTML('beforeend') : ajoute en dernier enfant */
  });
}

/* ============================================================
   FILTRAGE DYNAMIQUE DES DEMANDES
   ============================================================ */

/**
 * Filtre les demandes selon tous les contrôles de filtre actifs.
 * Appelée à chaque frappe (oninput) ou changement (onchange).
 */
function filtrerDemandes() {

  /* Lecture des valeurs de chaque filtre */
  const texte     = document.getElementById('rechercheDemandeInput').value.toLowerCase().trim();
  /* toLowerCase() + trim() : recherche insensible à la casse sans espaces parasites */
  const matiere   = document.getElementById('filtreMatiere').value;
  const filiere   = document.getElementById('filtreFiliere').value;
  const niveau    = document.getElementById('filtreNiveau').value;
  const jour      = document.getElementById('filtreJour').value;
  const heureDebut = document.getElementById('heureDebut').value;
  const heureFin   = document.getElementById('heureFin').value;

  /* Filtre le tableau en appliquant toutes les conditions */
  const demandesFiltrees = demandes.filter(function (demande) {

    /* Filtre texte : nom, matière ou description */
    const matchTexte = texte === '' ||
      demande.nom.toLowerCase().includes(texte) ||
      demande.matiere.toLowerCase().includes(texte) ||
      demande.description.toLowerCase().includes(texte);

    /* Filtre matière */
    const matchMatiere = matiere === '' || demande.matiereCode === matiere;

    /* Filtre filière */
    const matchFiliere = filiere === '' || demande.filiereCode === filiere;

    /* Filtre niveau */
    const matchNiveau = niveau === '' || demande.niveau === niveau;

    /* Filtre jour (au moins un créneau dans le jour sélectionné) */
    const matchJour = jour === '' ||
      demande.disponibilites.some(function (d) { return d.jourCode === jour; });
    /* some() : vrai si au moins un créneau correspond */

    /* Filtre heure de début */
    const matchHeureDebut = heureDebut === '' ||
      demande.disponibilites.some(function (d) { return d.debut <= heureDebut; });

    /* Filtre heure de fin */
    const matchHeureFin = heureFin === '' ||
      demande.disponibilites.some(function (d) { return d.fin >= heureFin; });

    /* Toutes les conditions doivent être vraies */
    return matchTexte && matchMatiere && matchFiliere && matchNiveau
        && matchJour && matchHeureDebut && matchHeureFin;
  });

  /* Réaffiche les demandes filtrées */
  afficherDemandes(demandesFiltrees);
}

/* ============================================================
   OFFRES CORRESPONDANTES À UNE DEMANDE
   ============================================================ */

/**
 * Trouve les offres qui correspondent à une demande et les affiche
 * dans le modal dédié, avec un bouton Accepter sur chacune.
 *
 * @param {number} demandeId - L'identifiant de la demande
 */
function voirOffresCorrespondantes(demandeId) {

  /* Trouve la demande dans le tableau */
  const demande = demandes.find(function (d) { return d.id === demandeId; });
  if (!demande) return; /* Sort si la demande n'existe pas */

  /* Titre du modal : personnalisé avec le nom de l'étudiant */
  document.getElementById('titreModalOffres').textContent =
    `Offres correspondant à la demande de ${demande.nom}`;

  /* Filtre les offres qui correspondent à la matière de la demande */
  const offresMatch = offresDisponibles.filter(function (offre) {
    return offre.matiereCode === demande.matiereCode;
    /* Match sur la matière : même code de matière = offre compatible */
  });

  /* Récupère la zone de contenu du modal */
  const contenu = document.getElementById('contenuOffresCorrespondantes');
  contenu.innerHTML = ''; /* Vide le contenu précédent */

  /* Si aucune offre ne correspond */
  if (offresMatch.length === 0) {
    contenu.innerHTML = `
      <div class="aucune-offre-msg">
        <i class="bi bi-emoji-frown fs-2 d-block mb-2"></i>
        <!-- Icône triste Bootstrap Icons -->
        Aucune offre ne correspond à cette demande pour le moment.
      </div>
    `;
    /* Affiche un message d'absence de résultat */
  } else {

    /* Génère une carte pour chaque offre correspondante */
    offresMatch.forEach(function (offre) {

      /* Lignes de disponibilités de l'offre */
      const dispos = offre.disponibilites
        .map(function (d) {
          return `<span class="dispo-item d-block">${d.jour} : ${d.debut} - ${d.fin}</span>`;
        })
        .join('');

      /* Calcule un score de compatibilité simulé (entre 75% et 98%) */
      const score = Math.floor(Math.random() * (98 - 75 + 1)) + 75;
      /* Math.random() : nombre aléatoire entre 0 et 1 */
      /* Math.floor() : arrondit à l'entier inférieur */

      /* HTML de la carte d'offre correspondante */
      const offreHTML = `
        <div class="offre-match-card">

          <!-- En-tête : avatar + nom + score -->
          <div class="offre-match-header">
            <div class="offre-match-user">
              <!-- Avatar coloré avec initiales -->
              <div class="card-avatar ${offre.avatarClass}" style="width:38px;height:38px;font-size:0.8rem;">
                ${offre.initiales}
              </div>
              <div>
                <div class="card-name" style="font-size:0.88rem;">${offre.nom}</div>
                <!-- Nom du mentor -->
                <div class="card-meta">
                  <span class="badge-meta">${offre.filiere}</span>
                  <span class="badge-meta">${offre.niveau}</span>
                </div>
              </div>
            </div>
            <!-- Score de compatibilité -->
            <span class="offre-match-score">${score}% compatible</span>
          </div>

          <!-- Description de l'offre -->
          <p class="offre-match-desc">${offre.description}</p>

          <!-- Disponibilités de l'offre -->
          <div class="dispos-title mb-1">
            <i class="bi bi-clock"></i>
            <span>Disponibilités</span>
          </div>
          <div class="mb-3" style="padding-left:20px;">
            ${dispos}
          </div>

          <!-- Boutons Accepter + Contacter -->
          <div class="d-flex gap-2">
            <button
              class="btn-accepter"
              onclick="accepterOffre(${offre.id}, ${demandeId})"
            >
              ✓ Accepter
              <!-- onclick : appelle accepterOffre() avec les deux IDs -->
            </button>
            <button
              class="btn-contacter-match"
              onclick="contacterMentor(${offre.id})"
            >
              Contacter
              <!-- onclick : ouvre la messagerie avec ce mentor -->
            </button>
          </div>

        </div>
        <!-- Fin offre-match-card -->
      `;

      /* Injecte la carte dans le modal */
      contenu.insertAdjacentHTML('beforeend', offreHTML);
    });
  }

  /* Ouvre le modal Bootstrap */
  const modal = document.getElementById('modalOffresCorrespondantes');
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
  /* bootstrap.Modal : classe Bootstrap pour contrôler les modals */
}

/* ============================================================
   MODAL : Publication d'une nouvelle demande
   ============================================================ */

/**
 * Ouvre le modal de publication d'une demande.
 */
function ouvrirModalPublier() {
  const modal = document.getElementById('modalPublier');
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
}

/**
 * Valide les champs et publie une nouvelle demande.
 * Appelée au clic sur le bouton "Publier" du modal.
 */
function publierDemande() {

  /* Récupère les valeurs de tous les champs */
  const titre       = document.getElementById('modalTitre').value.trim();       /* Titre de l'offre */
  const format      = document.getElementById('modalFormat').value;             /* Format de l'offre */
  const lacunes     = document.getElementById('modalLacunes').value;        /* Lacunes (id correct : modalMatiere) */
  const desc        = document.getElementById('modalDescription').value.trim(); /* Description */

  /* Validation : tous les champs sont obligatoires */
  if (!titre || !format || !lacunes || !desc) {
    alert('Veuillez remplir tous les champs avant de publier.');
    return; /* Arrête si des champs sont vides */
  }

  /* Dictionnaire : code matière → libellé lisible */
  const labelsMatiere = {
    'python': 'Python', 'javascript': 'JavaScript', 'sql': 'SQL',
    'dev-web': 'Développement Web', 'algorithmique': 'Algorithmique',
    'bdd': 'Base de données', 'reseaux': 'Réseaux', 'ia/mlrn': 'IA / Machine Learning',
    'si': 'Sécurité Informatique'
  };

  /* Dictionnaire : code matière → classe CSS du badge besoin */
  const classesBesoin = {
    'python': 'besoin-python', 'javascript': 'besoin-javascript', 'sql': 'besoin-sql',
    'dev-web': 'besoin-devweb', 'algorithmique': 'besoin-algorithmique',
    'bdd': 'besoin-bdd', 'reseaux': 'besoin-reseaux', 'ia/mlrn': 'besoin-ia/mlrn',
    'si': 'besoin-si'
  };

  /* Construit le nouvel objet demande */
  const nouvelleDemande = {
    id: demandes.length + 1,                   /* Nouvel ID unique */
    initiales: 'U',                            /* Initiale utilisateur */
    avatarClass: 'avatar-bleu',                /* Bleu par défaut */
    nom: 'Utilisateur',                        /* Nom de l'utilisateur */
    filiere: 'Ma filière',                     /* Filière de l'utilisateur */
    filiereCode: 'gl',                         /* Code filière par défaut */
    niveau: 'M1',                              /* Niveau par défaut */
    urgent: null,                             /* Pas urgent par défaut */
    matiere: labelsMatiere[lacunes] || lacunes, /* Libellé de la matière */
    matiereCode: lacunes,                      /* Code pour le filtrage */
    besoinClass: classesBesoin[matiere] || 'besoin-python', /* Classe CSS */
    description: description,                 /* Description saisie */
    disponibilites: []
  };

  /* Ajoute au tableau global */
  demandes.push(nouvelleDemande);

  /* Réaffiche toutes les demandes */
  afficherDemandes(demandes);

  /* Ferme le modal */
  const modal = document.getElementById('modalPublier');
  bootstrap.Modal.getInstance(modal).hide();

  /* Remet les champs à zéro */
  ['modalTitre','modalFormat','modalLacunes','modalDescription','modalJour','modalHeureDebut','modalHeureFin']
    .forEach(function(id) { document.getElementById(id).value = ''; });

  console.log('Nouvelle demande publiée :', nouvelleDemande);
}

/* ============================================================
   ACTIONS : Accepter une offre + Contacter un mentor
   ============================================================ */

/**
 * Accepte une offre correspondant à une demande.
 * Dans une vraie application, envoie une notification au mentor.
 *
 * @param {number} offreId   - ID de l'offre acceptée
 * @param {number} demandeId - ID de la demande concernée
 */
function accepterOffre(offreId, demandeId) {
  const offre   = offresDisponibles.find(function (o) { return o.id === offreId; });
  const demande = demandes.find(function (d) { return d.id === demandeId; });

  if (offre && demande) {
    alert(`✓ Offre de ${offre.nom} acceptée pour la demande de ${demande.nom} !\nUne notification a été envoyée au mentor.`);
    /* Dans une vraie app : appel API pour créer une session de mentorat */
    console.log(`Offre ${offreId} acceptée pour la demande ${demandeId}`);

    /* Ferme le modal après acceptation */
    const modal = document.getElementById('modalOffresCorrespondantes');
    bootstrap.Modal.getInstance(modal).hide();
  }
}

/**
 * Ouvre la messagerie pour contacter un mentor.
 *
 * @param {number} offreId - ID de l'offre du mentor à contacter
 */
function contacterMentor(offreId) {
  const offre = offresDisponibles.find(function (o) { return o.id === offreId; });
  if (offre) {
    alert(`Contacter ${offre.nom}...`);
    /* Dans une vraie app : window.location.href = 'messages.html?mentor=' + offreId; */
    console.log('Contacter mentor :', offre);
  }
}

/**
 * Affiche le profil d'un étudiant.
 *
 * @param {number} id - ID de la demande
 */
function voirProfil(id) {
  const demande = demandes.find(function (d) { return d.id === id; });
  if (demande) {
    alert(`Voir le profil de : ${demande.nom}`);
    console.log('Voir profil :', demande);
  }
}

/* ============================================================
   UTILITAIRE
   ============================================================ */

/**
 * Met en majuscule la première lettre d'une chaîne.
 *
 * @param {string} str - Chaîne à transformer
 * @returns {string} - Chaîne avec première lettre en majuscule
 */
function capitaliser(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
  /* charAt(0).toUpperCase() : première lettre en majuscule */
  /* slice(1) : reste de la chaîne inchangé */
}
