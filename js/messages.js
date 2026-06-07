'use strict';

/* DONNÉES SIMULÉES */

const CONVERSATIONS = [
  {
    id: 1,
    interlocuteur: { initiales: 'MH', nom: 'Marie Houngbédji', couleur: 'bleu', meta: 'GL · M1', enLigne: true },
    nonLus: 2,
    messages: [
      { id: 1, auteur: 'eux', texte: 'Bonjour ! Avez-vous eu le temps de regarder les exercices Pandas que je vous ai envoyés ?', heure: '14:22', date: 'Aujourd\'hui' },
      { id: 2, auteur: 'moi', texte: 'Oui, j\'ai commencé ! J\'ai une question sur les groupby.', heure: '14:35', date: 'Aujourd\'hui' },
      { id: 3, auteur: 'eux', texte: 'Pas de problème, on peut y revenir lors de notre prochaine session. Mardi à 17h, ça vous convient ?', heure: '14:36', date: 'Aujourd\'hui' },
    ]
  },
  {
    id: 2,
    interlocuteur: { initiales: 'PA', nom: 'Paul Adéoti', couleur: 'violet', meta: 'GL · L3', enLigne: false },
    nonLus: 0,
    messages: [
      { id: 1, auteur: 'moi',  texte: 'Bonjour Paul, je serais disponible mercredi soir pour la session SQL.', heure: 'Hier', date: 'Hier' },
      { id: 2, auteur: 'eux',  texte: 'Parfait, je prépare des exercices sur les jointures complexes.', heure: 'Hier', date: 'Hier' },
    ]
  },
  {
    id: 3,
    interlocuteur: { initiales: 'KM', nom: 'Kofi Mensah', couleur: 'indigo', meta: 'GL · L2', enLigne: false },
    nonLus: 0,
    messages: [
      { id: 1, auteur: 'eux', texte: 'La session d\'hier sur les arbres binaires était très utile, merci beaucoup !', heure: 'Il y a 2j', date: 'Il y a 2 jours' },
      { id: 2, auteur: 'moi', texte: 'Avec plaisir ! Continuez à pratiquer avec les exercices du TD.', heure: 'Il y a 2j', date: 'Il y a 2 jours' },
    ]
  },
];

/* ID de la conversation actuellement ouverte */
let conversationActive = null;

/* INITIALISATION */

document.addEventListener('DOMContentLoaded', function () {
  rendreListeConversations(CONVERSATIONS);
  ouvrirConversation(CONVERSATIONS[0].id);
});

/* LISTE DES CONVERSATIONS */

/**
 * Génère et injecte la liste des conversations.
 * @param {Array} liste - Tableau filtré de conversations
 */
function rendreListeConversations(liste) {
  const conteneur = document.getElementById('listeConversations');
  if (!conteneur) return;

  if (liste.length === 0) {
    conteneur.innerHTML = `<div class="etat-vide" style="padding: var(--s8) var(--s4);">
      <div class="etat-vide-titre">Aucune conversation</div>
    </div>`;
    return;
  }

  conteneur.innerHTML = liste.map(function (conv) {
    const dernierMsg  = conv.messages[conv.messages.length - 1];
    const apercu      = dernierMsg ? dernierMsg.texte : '';
    const actif       = conv.id === conversationActive ? 'actif' : '';
    const badgeNonLu  = conv.nonLus > 0
      ? `<span class="badge-non-lu">${conv.nonLus}</span>`
      : '';

    /* Point de statut (en ligne / hors ligne) */
    const pointStatut = conv.interlocuteur.enLigne
      ? 'statut-point--en-ligne'
      : 'statut-point--hors-ligne';

    return `
      <div class="conversation-item ${actif}" onclick="ouvrirConversation(${conv.id})">
        <div style="position:relative; flex-shrink:0;">
          <div class="avatar avatar--sm avatar--${conv.interlocuteur.couleur}">
            ${conv.interlocuteur.initiales}
          </div>
          <div class="statut-point ${pointStatut}" style="position:absolute; bottom:0; right:0; border:2px solid var(--fond-carte);"></div>
        </div>
        <div class="conversation-info">
          <div class="conversation-nom">${conv.interlocuteur.nom}</div>
          <div class="conversation-apercu">${apercu}</div>
        </div>
        <div class="conversation-meta">
          <span class="conversation-heure">${dernierMsg ? dernierMsg.heure : ''}</span>
          ${badgeNonLu}
        </div>
      </div>
    `;
  }).join('');
}

/**
 * Filtre les conversations selon la saisie dans le champ de recherche.
 */
function filtrerConversations() {
  const texte = document.getElementById('rechercheConversation')?.value.toLowerCase().trim() ?? '';
  const filtrées = CONVERSATIONS.filter(function (c) {
    return c.interlocuteur.nom.toLowerCase().includes(texte);
  });
  rendreListeConversations(filtrées);
}

window.filtrerConversations = filtrerConversations;

/* CHAT : OUVERTURE D'UNE CONVERSATION */

/**
 * Ouvre une conversation et affiche ses messages dans la zone de chat.
 * @param {number} id - ID de la conversation
 */
function ouvrirConversation(id) {
  conversationActive = id;

  /* Marque la conversation comme lue */
  const conv = CONVERSATIONS.find(function (c) { return c.id === id; });
  if (!conv) return;
  conv.nonLus = 0;

  /* Met à jour la liste (pour retirer le badge non lu) */
  rendreListeConversations(CONVERSATIONS);

  /* Rend l'en-tête du chat */
  rendreChatEntete(conv);

  /* Rend les messages */
  rendreChatMessages(conv);

  /* Focus sur le champ de saisie */
  document.getElementById('champMessage')?.focus();
}

window.ouvrirConversation = ouvrirConversation;

/**
 * Construit et injecte l'en-tête de la fenêtre de chat.
 * @param {Object} conv
 */
function rendreChatEntete(conv) {
  const entete = document.getElementById('chatEntete');
  if (!entete) return;

  const inter = conv.interlocuteur;
  const statutTexte = inter.enLigne ? 'En ligne' : 'Hors ligne';
  const statutClasse = inter.enLigne ? 'statut-point--en-ligne' : 'statut-point--hors-ligne';

  entete.innerHTML = `
    <div class="avatar avatar--md avatar--${inter.couleur}">${inter.initiales}</div>
    <div style="flex:1">
      <div class="chat-entete-nom">${inter.nom}</div>
      <div class="chat-entete-meta flex items-centre gap-2">
        <span class="statut-point ${statutClasse}"></span>
        ${statutTexte} · ${inter.meta}
      </div>
    </div>
  `;
}

/**
 * Construit et injecte les bulles de messages.
 * @param {Object} conv
 */
function rendreChatMessages(conv) {
  const zone = document.getElementById('chatMessages');
  if (!zone) return;

  let dateActuelle = null;
  let html = '';

  conv.messages.forEach(function (msg) {
    /* Séparateur de date si nouvelle date */
    if (msg.date !== dateActuelle) {
      html += `<div class="separateur-date">${msg.date}</div>`;
      dateActuelle = msg.date;
    }

    const cote = msg.auteur === 'moi' ? 'bulle--envoye' : 'bulle--recu';

    html += `
      <div class="bulle ${cote}">
        <div class="bulle-texte">${msg.texte}</div>
        <div class="bulle-heure">${msg.heure}</div>
      </div>
    `;
  });

  zone.innerHTML = html;

  /* Scroll automatique vers le bas */
  zone.scrollTop = zone.scrollHeight;
}

/* ENVOI D'UN MESSAGE */

/**
 * Envoie un message dans la conversation active.
 * Dans une vraie app : POST /api/messages/
 */
function envoyerMessage() {
  const champ = document.getElementById('champMessage');
  if (!champ) return;

  const texte = champ.value.trim();
  if (!texte || conversationActive === null) return;

  /* Cherche la conversation active */
  const conv = CONVERSATIONS.find(function (c) { return c.id === conversationActive; });
  if (!conv) return;

  /* Ajoute le message au tableau */
  const now = new Date();
  const heure = now.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });

  conv.messages.push({
    id:     conv.messages.length + 1,
    auteur: 'moi',
    texte:  texte,
    heure:  heure,
    date:   'Aujourd\'hui'
  });

  /* Vide le champ et re-rend le chat */
  champ.value = '';
  rendreChatMessages(conv);
  rendreListeConversations(CONVERSATIONS);

  /* Simule une réponse après 1.5s (démo) */
  setTimeout(function () {
    simulerReponse(conv);
  }, 1500);
}

/**
 * Simule une réponse automatique de l'interlocuteur (démo uniquement).
 * @param {Object} conv
 */
function simulerReponse(conv) {
  const reponsesDeDemo = [
    'Bien reçu, merci !',
    'D\'accord, je prends note.',
    'Parfait, à bientôt.',
    'On en reparle lors de la prochaine session.',
  ];

  const texte = reponsesDeDemo[Math.floor(Math.random() * reponsesDeDemo.length)];
  const heure = new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });

  conv.messages.push({
    id:     conv.messages.length + 1,
    auteur: 'eux',
    texte,
    heure,
    date:   'Aujourd\'hui'
  });

  rendreChatMessages(conv);
}

/**
 * Envoie le message en appuyant sur Entrée.
 * @param {KeyboardEvent} e
 */
function envoyerSiEntree(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    envoyerMessage();
  }
}

window.envoyerMessage   = envoyerMessage;
window.envoyerSiEntree  = envoyerSiEntree;