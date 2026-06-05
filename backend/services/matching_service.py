from db.database import get_connection

def calculer_correspondances(utilisateur_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Récupère les difficultés de l'utilisateur
    cursor.execute("""
        SELECT matiere_id FROM difficultes_utilisateur
        WHERE utilisateur_id = %s
    """, (utilisateur_id,))
    difficultes = [r['matiere_id'] for r in cursor.fetchall()]

    if not difficultes:
        conn.close()
        return

    # Trouve les mentors ayant ces compétences
    format_ids = ','.join(['%s'] * len(difficultes))
    cursor.execute(f"""
        SELECT DISTINCT u.id,
               COUNT(cu.matiere_id) as nb_match
        FROM utilisateurs u
        JOIN competences_utilisateur cu ON cu.utilisateur_id = u.id
        WHERE cu.matiere_id IN ({format_ids})
        AND u.id != %s AND u.est_actif = 1
        GROUP BY u.id
    """, (*difficultes, utilisateur_id))
    mentors = cursor.fetchall()

    total_matieres = len(difficultes)

    for mentor in mentors:
        score = (mentor['nb_match'] / total_matieres) * 100

        # Vérifie si la correspondance existe déjà
        cursor.execute("""
            SELECT id FROM correspondances
            WHERE mentor_id = %s AND mentee_id = %s
        """, (mentor['id'], utilisateur_id))
        existant = cursor.fetchone()

        if existant:
            cursor.execute("""
                UPDATE correspondances SET score_compatibilite = %s
                WHERE mentor_id = %s AND mentee_id = %s
            """, (score, mentor['id'], utilisateur_id))
        else:
            cursor.execute("""
                INSERT INTO correspondances (mentor_id, mentee_id, score_compatibilite)
                VALUES (%s, %s, %s)
            """, (mentor['id'], utilisateur_id, score))

    conn.commit()
    conn.close()