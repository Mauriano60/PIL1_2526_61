from db.database import get_connection

def calculer_correspondances(utilisateur_id):
    """
    Calcule les correspondances mentor/mentee pour un utilisateur donné.
    Le score de compatibilité est basé sur :
    - Les compétences du mentor qui correspondent aux difficultés du mentee (40%)
    - La compatibilité des disponibilités (30%)
    - La proximité de filière (20%)
    - La proximité de niveau d'études (10%)
    """

    # Validation de l'entrée
    if not utilisateur_id or not isinstance(utilisateur_id, int):
        print("Erreur : utilisateur_id invalide")
        return

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ── 1. Récupérer les infos de l'utilisateur (mentee) ──────────────
        cursor.execute("""
            SELECT id, id_filiere, id_niveau
            FROM utilisateurs
            WHERE id = %s AND est_actif = 1
        """, (utilisateur_id,))
        mentee = cursor.fetchone()

        # Si l'utilisateur n'existe pas ou est inactif, on arrête
        if not mentee:
            print(f"Utilisateur {utilisateur_id} introuvable ou inactif")
            return

        # ── 2. Récupérer les matières difficiles du mentee ─────────────────
        cursor.execute("""
            SELECT matiere_id
            FROM difficultes_utilisateur
            WHERE utilisateur_id = %s
        """, (utilisateur_id,))
        # Extraire juste les IDs dans une liste
        difficultes = [r['matiere_id'] for r in cursor.fetchall()]

        # Si le mentee n'a aucune difficulté déclarée, pas de matching possible
        if not difficultes:
            print(f"Aucune difficulté déclarée pour l'utilisateur {utilisateur_id}")
            return

        # ── 3. Récupérer les disponibilités du mentee ──────────────────────
        cursor.execute("""
            SELECT jour_semaine, heure_debut, heure_fin
            FROM disponibilites
            WHERE utilisateur_id = %s
        """, (utilisateur_id,))
        # Stocker les disponibilités du mentee sous forme de liste
        dispos_mentee = cursor.fetchall()

        # ── 4. Trouver les mentors potentiels ─────────────────────────────
        # Un mentor potentiel est un utilisateur actif différent du mentee
        # qui a au moins une compétence correspondant aux difficultés du mentee
        placeholders = ','.join(['%s'] * len(difficultes))
        query = f"""
            SELECT DISTINCT u.id, u.id_filiere, u.id_niveau,
                   COUNT(cu.matiere_id) as nb_competences_match
            FROM utilisateurs u
            JOIN competences_utilisateur cu ON cu.utilisateur_id = u.id
            WHERE cu.matiere_id IN ({placeholders})
            AND u.id != %s
            AND u.est_actif = 1
            GROUP BY u.id, u.id_filiere, u.id_niveau
        """
        # Paramètres : les IDs des matières difficiles + l'ID du mentee
        params = tuple(difficultes) + (utilisateur_id,)
        cursor.execute(query, params)
        mentors_potentiels = cursor.fetchall()

        # Si aucun mentor trouvé, on arrête
        if not mentors_potentiels:
            print(f"Aucun mentor trouvé pour l'utilisateur {utilisateur_id}")
            return

        # Nombre total de matières difficiles du mentee (pour le calcul du score)
        total_difficultes = len(difficultes)

        # ── 5. Calculer le score pour chaque mentor ────────────────────────
        for mentor in mentors_potentiels:

            # ── 5a. Score compétences (40%) ────────────────────────────────
            # Proportion des difficultés du mentee couvertes par le mentor
            score_competences = (mentor['nb_competences_match'] / total_difficultes) * 40

            # ── 5b. Score disponibilités (30%) ─────────────────────────────
            # Récupérer les disponibilités du mentor
            cursor.execute("""
                SELECT jour_semaine, heure_debut, heure_fin
                FROM disponibilites
                WHERE utilisateur_id = %s
            """, (mentor['id'],))
            dispos_mentor = cursor.fetchall()

            # Compter les créneaux compatibles entre mentor et mentee
            creneaux_compatibles = 0
            for dispo_mentee in dispos_mentee:
                for dispo_mentor in dispos_mentor:
                    # Vérifier si le jour est le même
                    meme_jour = dispo_mentee['jour_semaine'] == dispo_mentor['jour_semaine']
                    # Vérifier si les horaires se chevauchent
                    chevauchement = (
                        dispo_mentee['heure_debut'] < dispo_mentor['heure_fin'] and
                        dispo_mentee['heure_fin'] > dispo_mentor['heure_debut']
                    )
                    # Si le jour et les horaires correspondent, c'est compatible
                    if meme_jour and chevauchement:
                        creneaux_compatibles += 1

            # Calculer le score disponibilités
            # Si le mentee n'a pas de disponibilités, score neutre de 15/30
            if len(dispos_mentee) == 0:
                score_dispos = 15
            else:
                # Proportion de créneaux compatibles * 30
                score_dispos = min((creneaux_compatibles / len(dispos_mentee)) * 30, 30)

            # ── 5c. Score filière (20%) ────────────────────────────────────
            # Même filière = score plein, sinon 0
            if mentor['id_filiere'] == mentee['id_filiere']:
                score_filiere = 20  # Même filière
            else:
                score_filiere = 0   # Filière différente

            # ── 5d. Score niveau d'études (10%) ───────────────────────────
            # Calculer la différence de niveau entre mentor et mentee
            difference_niveau = abs(mentor['id_niveau'] - mentee['id_niveau'])

            # Plus la différence est faible, meilleur est le score
            if difference_niveau == 0:
                score_niveau = 5    # Même niveau (peu recommandé mais possible)
            elif difference_niveau == 1:
                score_niveau = 10   # Un niveau d'écart (idéal)
            elif difference_niveau == 2:
                score_niveau = 7    # Deux niveaux d'écart
            else:
                score_niveau = 3    # Grande différence de niveau

            # ── 5e. Score total ────────────────────────────────────────────
            # Somme des 4 composantes (max = 100)
            score_total = round(
                score_competences + score_dispos + score_filiere + score_niveau,
                2
            )

            # S'assurer que le score est entre 0 et 100
            score_total = max(0, min(100, score_total))

            # ── 6. Enregistrer ou mettre à jour la correspondance ──────────
            # Vérifier si une correspondance existe déjà entre ce mentor et ce mentee
            cursor.execute("""
                SELECT id FROM correspondances
                WHERE mentor_id = %s AND mentee_id = %s
            """, (mentor['id'], utilisateur_id))
            existant = cursor.fetchone()

            if existant:
                # Mettre à jour le score existant
                cursor.execute("""
                    UPDATE correspondances
                    SET score_compatibilite = %s
                    WHERE mentor_id = %s AND mentee_id = %s
                """, (score_total, mentor['id'], utilisateur_id))
            else:
                # Créer une nouvelle correspondance
                cursor.execute("""
                    INSERT INTO correspondances (mentor_id, mentee_id, score_compatibilite)
                    VALUES (%s, %s, %s)
                """, (mentor['id'], utilisateur_id, score_total))

        # Sauvegarder toutes les modifications en base
        conn.commit()
        print(f"Matching calculé avec succès pour l'utilisateur {utilisateur_id}")

    except Exception as e:
        # Afficher l'erreur sans crasher l'application
        print(f"Erreur lors du calcul du matching : {str(e)}")
    finally:
        # Toujours fermer la connexion même en cas d'erreur
        if conn:
            conn.close()