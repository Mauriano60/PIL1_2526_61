'use strict';

const NOTIFICATIONS = [
  { id:1, type:'matching', lu:false, texte:'<strong>Marie Houngbédji</strong> correspond à 94% de votre profil en Python.', heure:'Il y a 32 min' },
  { id:2, type:'demande',  lu:false, texte:'<strong>Adjoa Mensah</strong> vous a envoyé une demande de mentorat en Python.', heure:'Il y a 1h' },
  { id:3, type:'message',  lu:false, texte:'Nouveau message de <strong>Paul Adéoti</strong> : "Parfait, je prépare des exercices…"', heure:'Il y a 2h' },
  { id:4, type:'matching', lu:true,  texte:'7 nouveaux profils compatibles ont été trouvés cette semaine.', heure:'Hier' },
  { id:5, type:'demande',  lu:true,  texte:'<strong>Paul Adéoti</strong> a accepté votre demande de mentorat.', heure:'Hier' },
  { id:6, type:'systeme',  lu:true,  texte:'Votre profil a été mis à jour avec succès.', heure:'Il y a 2 jours' },
  { id:7, type:'message',  lu:true,  texte:'<strong>Kofi Mensah</strong> : "La session d\'hier était très utile, merci !"', heure:'Il y a 2 jours' },
];

const ICONES = {
  matching: '✦',
  message:  '◉',
  demande:  '◈',
  systeme:  '◇',
};

let filtreActif = 'toutes';

document.addEventListener('DOMContentLoaded', function () {
  rendreNotifications();
});

function filtrerNotifs(filtre, el) {
  filtreActif = filtre;
  document.querySelectorAll('.onglet').forEach(function (b) { b.classList.remove('actif'); });
  el.classList.add('actif');
  rendreNotifications();
}

function rendreNotifications() {
  const conteneur = document.getElementById('listeNotifications');
  if (!conteneur) return;

  let liste = NOTIFICATIONS.filter(function (n) {
    if (filtreActif === 'toutes')   return true;
    if (filtreActif === 'non-lues') return !n.lu;
    return n.type === filtreActif;
  });

  if (liste.length === 0) {
    conteneur.innerHTML = `<div class="etat-vide"><div class="etat-vide-titre">Aucune notification</div><div class="etat-vide-description">Rien de nouveau pour le moment.</div></div>`;
    return;
  }

  conteneur.innerHTML = liste.map(function (n) {
    return `
      <div class="notif-item ${n.lu ? '' : 'non-lue'}" onclick="marquerLu(${n.id}, this)">
        <div class="notif-type-point notif-type-point--${n.type}">${ICONES[n.type] || '◇'}</div>
        <div class="notif-corps">
          <div class="notif-texte">${n.texte}</div>
          <div class="notif-heure">${n.heure}</div>
        </div>
        ${n.lu ? '' : '<div class="notif-dot-non-lu"></div>'}
      </div>
    `;
  }).join('');
}

function marquerLu(id, el) {
  const notif = NOTIFICATIONS.find(function (n) { return n.id === id; });
  if (notif) {
    notif.lu = true;
    el.classList.remove('non-lue');
    el.querySelector('.notif-dot-non-lu')?.remove();
  }
}

function toutMarquerLu() {
  NOTIFICATIONS.forEach(function (n) { n.lu = true; });
  rendreNotifications();
  afficherToast('Toutes les notifications ont été marquées comme lues.', 'succes');
}

window.filtrerNotifs  = filtrerNotifs;
window.marquerLu      = marquerLu;
window.toutMarquerLu  = toutMarquerLu;