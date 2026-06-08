/* ============================================================
   settings-compte.js — Logique de la section "Compte"
   IFRI MentorLink — Paramètres
   ============================================================ */

/* ── Affichage du toast de confirmation ── */
function afficherToast(message = '✓ Modifications enregistrées') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2800);
}

/* ── Changement de photo de profil ── */
document.getElementById('btnChangePhoto').addEventListener('click', () => {
  document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function () {
  if (!this.files || !this.files[0]) return;

  /* Vérification du poids (2 Mo max) */
  if (this.files[0].size > 2 * 1024 * 1024) {
    alert('Le fichier dépasse 2 Mo. Veuillez choisir une image plus légère.');
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    /* Mise à jour de l'avatar dans la section */
    const avatarLg = document.getElementById('avatarLg');
    avatarLg.innerHTML = `<img src="${e.target.result}" alt="Avatar utilisateur" />`;

    /* Mise à jour de l'avatar dans la topbar */
    const topAvatar = document.getElementById('topAvatar');
    topAvatar.style.backgroundImage  = `url(${e.target.result})`;
    topAvatar.style.backgroundSize   = 'cover';
    topAvatar.style.backgroundPosition = 'center';
    topAvatar.textContent = '';
  };
  reader.readAsDataURL(this.files[0]);
});

/* ── Sélection / désélection des tags (compétences & besoins) ── */
document.querySelectorAll('.tag').forEach((tag) => {
  tag.addEventListener('click', () => {
    tag.classList.toggle('selected');
  });
});

/* ── Ajout d'un créneau de disponibilité ── */
document.getElementById('btnAddSlot').addEventListener('click', ajouterCreneau);

function ajouterCreneau() {
  const liste = document.getElementById('slotList');
  const carte = document.createElement('div');
  carte.className = 'slot-card';

  carte.innerHTML = `
    <div class="slot-field">
      <label>Jour</label>
      <select>
        <option value="">Sélectionnez...</option>
        <option>Lundi</option>
        <option>Mardi</option>
        <option>Mercredi</option>
        <option>Jeudi</option>
        <option>Vendredi</option>
        <option>Samedi</option>
        <option>Dimanche</option>
      </select>
    </div>
    <div class="slot-field">
      <label>Début</label>
      <input type="time" />
    </div>
    <div class="slot-field">
      <label>Fin</label>
      <input type="time" />
    </div>
    <button class="slot-delete" title="Supprimer ce créneau">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
        <polyline points="3 6 5 6 21 6"/>
        <path d="M19 6l-1 14H6L5 6"/>
        <path d="M10 11v6"/>
        <path d="M14 11v6"/>
        <path d="M9 6V4h6v2"/>
      </svg>
    </button>
  `;

  /* Suppression du créneau au clic sur la corbeille */
  carte.querySelector('.slot-delete').addEventListener('click', () => {
    carte.remove();
  });

  liste.appendChild(carte);
}

/* ── Collecte des données du formulaire et simulation d'enregistrement ── */
function collecterDonnees() {
  return {
    nom:         document.getElementById('nom').value.trim(),
    prenom:      document.getElementById('prenom').value.trim(),
    email:       document.getElementById('email').value.trim(),
    telephone:   document.getElementById('telephone').value.trim(),
    filiere:     document.getElementById('filiere').value,
    niveau:      document.getElementById('niveau').value,
    biographie:  document.getElementById('biographie').value.trim(),
    competences: [...document.querySelectorAll('#tagsCompetences .tag.selected')]
                   .map(t => t.dataset.value),
    besoins:     [...document.querySelectorAll('#tagsBesoins .tag.selected')]
                   .map(t => t.dataset.value),
    creneaux:    [...document.querySelectorAll('.slot-card')].map(carte => ({
      jour:  carte.querySelector('select').value,
      debut: carte.querySelectorAll('input[type="time"]')[0].value,
      fin:   carte.querySelectorAll('input[type="time"]')[1].value,
    })),
  };
}

function enregistrer() {
  const donnees = collecterDonnees();
  console.log('[MentorLink] Données compte à envoyer à l\'API :', donnees);
  /* TODO : remplacer par un fetch() vers /api/accounts/profile/ (méthode PATCH) */
  afficherToast('✓ Modifications enregistrées');
}

/* Déclenchement depuis les deux boutons Enregistrer */
document.getElementById('btnSaveTop').addEventListener('click', enregistrer);
document.getElementById('btnSaveBottom').addEventListener('click', enregistrer);