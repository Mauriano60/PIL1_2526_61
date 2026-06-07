# CHABI AYEDOUN Yoéla
from db.database import fetch_all, fetch_one, execute

def calculer_correspondances(utilisateur_id):
    """
    Calcule les correspondances mentor/mentee pour un utilisateur donné.
    Le matching se base dynamiquement sur les matières présentes dans ses 
    demandes de mentorat actives.
    """

    # Validation de sécurité de l'entrée
    if not utilisateur_id or not isinstance(utilisateur_id, int):
        print("Erreur : utilisateur_id invalide")
        return

    try:
        # ── 1. Récupérer les infos de l'utilisateur connecté (mentee) ──────
        mentee = fetch_one("""
            SELECT id, id_filiere, id_niveau
            FROM utilisateurs
            WHERE id = %s AND est_actif = 1
        """, (utilisateur_id,))

        if not mentee:
            print(f"Utilisateur {utilisateur_id} introuvable ou inactif")
            return

        # ── 2. Récupérer les matières de ses DEMANDES de mentorat actives ──
        res_demandes = fetch_all("""
            SELECT DISTINCT matiere_id
            FROM demande_mentorat
            WHERE utilisateur_id = %s
        """, (utilisateur_id,))
        
        matieres_demandees = [r['matiere_id'] for r in res_demandes]

        # Si l'utilisateur n'a aucune demande active, pas de calcul nécessaire
        if not matieres_demandees:
            print(f"Aucune demande de mentorat active pour l'utilisateur {utilisateur_id}")
            return

        # ── 3. Récupérer les disponibilités de l'utilisateur connecté ──────
        dispos_mentee = fetch_all("""
            SELECT jour_semaine, heure_debut, heure_fin
            FROM disponibilites
            WHERE utilisateur_id = %s
        """, (utilisateur_id,))

        # ── 4. Trouver les mentors potentiels en base de données ──────────
        placeholders = ','.join(['%s'] * len(matieres_demandees))
        query = f"""
            SELECT DISTINCT u.id, u.id_filiere, u.id_niveau,
                   COUNT(DISTINCT om.matiere_id) as nb_competences_match
            FROM utilisateurs u
            LEFT JOIN offre_mentorat om ON om.utilisateur_id = u.id AND om.matiere_id IN ({placeholders})
            LEFT JOIN competences_utilisateur cu ON cu.utilisateur_id = u.id AND cu.matiere_id IN ({placeholders})
            WHERE (om.id IS NOT NULL OR cu.matiere_id IS NOT NULL)
            AND u.id != %s
            AND u.est_actif = 1
            GROUP BY u.id, u.id_filiere, u.id_niveau
        """
        params = tuple(matieres_demandees) + tuple(matieres_demandees) + (utilisateur_id,)
        mentors_potentiels = fetch_all(query, params)

        if not mentors_potentiels:
            print(f"Aucun mentor correspondant aux demandes de l'utilisateur {utilisateur_id}")
            return

        total_matieres = len(matieres_demandees)

        # ── 5. Calculer et enregistrer les scores pour chaque mentor ──────
        for mentor in mentors_potentiels:

            # ── 5a. Score compétences / offres (40%) ───────────────────────
            score_competences = (mentor['nb_competences_match'] / total_matieres) * 40

            # ── 5b. Score disponibilités (30%) ─────────────────────────────
            # Utilisation directe de fetch_all au lieu de cursor.execute
            dispos_mentor = fetch_all("""
                SELECT jour_semaine, heure_debut, heure_fin
                FROM disponibilites
                WHERE utilisateur_id = %s
            """, (mentor['id'],))

            creneaux_compatibles = 0
            for d_mentee in dispos_mentee:
                for d_mentor in dispos_mentor:
                    meme_jour = d_mentee['jour_semaine'] == d_mentor['jour_semaine']
                    chevauchement = (
                        d_mentee['heure_debut'] < d_mentor['heure_fin'] and
                        d_mentee['heure_fin'] > d_mentor['heure_debut']
                    )
                    if meme_jour and chevauchement:
                        creneaux_compatibles += 1

            if len(dispos_mentee) == 0:
                score_dispos = 15  
            else:
                score_dispos = min((creneaux_compatibles / len(dispos_mentee)) * 30, 30)

            # ── 5c. Score filière (20%) ────────────────────────────────────
            score_filiere = 20 if mentor['id_filiere'] == mentee['id_filiere'] else 0

            # ── 5d. Score niveau d'études (10%) ───────────────────────────
            difference_niveau = mentor['id_niveau'] - mentee['id_niveau']

            if difference_niveau == 1:
                score_niveau = 10   # +1 niveau au-dessus -> Idéal
            elif difference_niveau == 2:
                score_niveau = 8    # +2 niveaux au-dessus -> Très bien
            elif difference_niveau == 0:
                score_niveau = 5    # Même niveau d'études (Entraide)
            else:
                score_niveau = 2    # Niveau inférieur

            # ── 5e. Score total final ──────────────────────────────────────
            score_total = round(score_competences + score_dispos + score_filiere + score_niveau, 2)
            score_total = max(0, min(100, score_total))

            # ── 6. Insertion ou Mise à jour de la correspondance ───────────
            # Utilisation directe de fetch_one et execute de ton module db.database
            existant = fetch_one("""
                SELECT id FROM correspondances
                WHERE mentor_id = %s AND mentee_id = %s
            """, (mentor['id'], utilisateur_id))

            if existant:
                execute("""
                    UPDATE correspondances
                    SET score_compatibilite = %s
                    WHERE mentor_id = %s AND mentee_id = %s
                """, (score_total, mentor['id'], utilisateur_id))
            else:
                execute("""
                    INSERT INTO correspondances (mentor_id, mentee_id, score_compatibilite)
                    VALUES (%s, %s, %s)
                """, (mentor['id'], utilisateur_id, score_total))

        print(f"Matching dynamique calculé avec succès pour l'utilisateur {utilisateur_id}")

    except Exception as e:
        print(f"Erreur critique lors du calcul du matching : {str(e)}")